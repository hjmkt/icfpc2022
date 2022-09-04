from common import *
from util import *
import cv2
import numpy as np
import sys
from concurrent.futures import ProcessPoolExecutor


def compute_score_diff(canvas, target, rect, merge_cost_offset=600, alternative_cost=False):
    [[x, y, width, height], [r, g, b, a]] = rect
    current_pixels = canvas.pixels[y:y+height, x:x+width]
    cand_pixels = np.zeros((height, width, 4))
    cand_pixels[:, :] = [r, g, b, a]
    target_pixels = target[y:y+height, x:x+width]
    current_diff = np.sqrt(((target_pixels-current_pixels)**2).sum(axis=-1)).sum() * 0.005
    cand_diff = np.sqrt(((target_pixels-cand_pixels)**2).sum(axis=-1)).sum() * 0.005
    first_rect_size = max((x+width)*(y+height), (canvas.width-x)*(y+height), (x+width)*(canvas.height-y), (canvas.width-x)*(canvas.height-y))
    pcut_alpha = 3 if alternative_cost else 10
    cost = round(pcut_alpha*1) + round(pcut_alpha * canvas.width * canvas.height / first_rect_size)
    color_alpha = 5
    cost += round(color_alpha * canvas.width * canvas.height / width / height)
    # merge_cost = round(1*0.005) + round(1 * canvas.width * canvas.height / first_rect_size)
    # merge_cost = cost*2 + merge_cost_offset # FIXME
    merge_cost = cost + 100#*2 + merge_cost_offset # FIXME
    # merge_cost = 0
    score_diff = cand_diff - current_diff + cost + merge_cost
    return score_diff

def refine(canvas_target_start_rect):
    canvas, target, start_rect, merge_cost_offset, alternative_cost = canvas_target_start_rect
    rect = start_rect
    local_best_diff = compute_score_diff(canvas, target, rect, merge_cost_offset, alternative_cost)
    for step in [16, 4, 1]:
    # for step in [4, 1]:
        while True:
            [[x, y, width, height], [r, g, b, a]] = rect
            cand_rects = []
            if x>=step:
                cand_rects.append([[x-step, y, width+1, height], [r, g, b, a]])
            if y>=step:
                cand_rects.append([[x, y-step, width, height+1], [r, g, b, a]])
            if x+width+step<=canvas.width:
                cand_rects.append([[x, y, width+step, height], [r, g, b, a]])
            if y+height+step<=canvas.height:
                cand_rects.append([[x, y, width, height+step], [r, g, b, a]])
            if width>step:
                cand_rects.append([[x+step, y, width-step, height], [r, g, b, a]])
                cand_rects.append([[x, y, width-step, height], [r, g, b, a]])
            if height>step:
                cand_rects.append([[x, y+step, width, height-step], [r, g, b, a]])
                cand_rects.append([[x, y, width, height-step], [r, g, b, a]])
            if r>=step:
                cand_rects.append([[x, y, width, height], [r-step, g, b, a]])
            if g>=step:
                cand_rects.append([[x, y, width, height], [r, g-step, b, a]])
            if b>=step:
                cand_rects.append([[x, y, width, height], [r, g, b-step, a]])
            if a>=step:
                cand_rects.append([[x, y, width, height], [r, g, b, a-step]])
            if r<=255-step:
                cand_rects.append([[x, y, width, height], [r+step, g, b, a]])
            if g<=255-step:
                cand_rects.append([[x, y, width, height], [r, g+step, b, a]])
            if b<=255-step:
                cand_rects.append([[x, y, width, height], [r, g, b+step, a]])
            if a<=255-step:
                cand_rects.append([[x, y, width, height], [r, g, b, a+step]])
            tmp_best_rect = rect
            tmp_best_diff = local_best_diff
            for cand_rect in cand_rects:
                diff = compute_score_diff(canvas, target, cand_rect)
                if diff<tmp_best_diff:
                    tmp_best_diff = diff
                    tmp_best_rect = cand_rect
            if tmp_best_diff==local_best_diff:
                break
            rect[0] = tmp_best_rect[0]
            rect[1] = tmp_best_rect[1]
            if tmp_best_diff<local_best_diff:
                local_best_diff = tmp_best_diff
                # print("local", rect, local_best_diff, file=sys.stderr)
            else:
                break
    return rect, local_best_diff


def find_cand_rect(canvas, target, num_seeds=64, merge_cost_offset=600, alternative_cost=False):
    start_rects = [[[np.random.randint(0, canvas.width), np.random.randint(0, canvas.height), 1, 1], np.random.randint(0, 256, (4))] for _ in range(num_seeds)]
    
    best_rect = None
    best_diff = 1e8
    with ProcessPoolExecutor(8) as executor:
        results = executor.map(refine, map(lambda x: (canvas, target, x, merge_cost_offset, alternative_cost), start_rects))
    for (local_best_rect, local_best_diff) in results:
        if local_best_diff<best_diff:
            best_diff = local_best_diff
            best_rect = local_best_rect
            print(best_rect, best_diff, file=sys.stderr)

    return (best_rect, best_diff)

def rect_to_moves(canvas, rect):
    [[x, y, width, height], color] = rect
    if x==0:
        if x+width==canvas.width:
            if y==0:
                if y+height==canvas.height:
                    return [
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}", "color": color}),
                    ]
                else:
                    return [
                        Move("lcut", {"block_id": canvas.coord_to_block_id[y][x], "orientation": "horizontal", "offset": y+height}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                    ]
            else:
                if y+height==canvas.height:
                    return [
                        Move("lcut", {"block_id": canvas.coord_to_block_id[y][x], "orientation": "horizontal", "offset": y}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                    ]
                else:
                    return [
                        Move("lcut", {"block_id": canvas.coord_to_block_id[y][x], "orientation": "horizontal", "offset": y}),
                        Move("lcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1", "orientation": "horizontal", "offset": y+height}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.1.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.0"}),
                    ]
        else:
            if y==0:
                if y+height==canvas.height:
                    return [
                        Move("lcut", {"block_id": canvas.coord_to_block_id[y][x], "orientation": "vertical", "offset": x+width}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                    ]
                else:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x+width, y+height]}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.global_id+2}"}),
                    ]
            else:
                if y+height==canvas.height:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x+width, y]}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.3", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.global_id+2}"}),
                    ]
                else:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x+width, y]}),
                        Move("lcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.3", "orientation": "horizontal", "offset": y+height}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.3.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.3.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.2"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+2}", "block_id1": f"{canvas.global_id+3}"}),
                    ]
    else:
        if x+width==canvas.width:
            if y==0:
                if y+height==canvas.height:
                    return [
                        Move("lcut", {"block_id": canvas.coord_to_block_id[y][x], "orientation": "vertical", "offset": x}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                    ]
                else:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x, y+height]}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.global_id+2}"}),
                    ]
            else:
                if y+height==canvas.height:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x, y]}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.global_id+2}"}),
                    ]
                else:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x, y]}),
                        Move("lcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2", "orientation": "horizontal", "offset": y+height}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.2.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+2}", "block_id1": f"{canvas.global_id+3}"}),
                    ]
        else:
            if y==0:
                if y+height==canvas.height:
                    return [
                        Move("lcut", {"block_id": canvas.coord_to_block_id[y][x], "orientation": "vertical", "offset": x}),
                        Move("lcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1", "orientation": "vertical", "offset": x+width}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.1.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.0"}),
                    ]
                else:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x, y+height]}),
                        Move("lcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1", "orientation": "vertical", "offset": x+width}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.1.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.1.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.0"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+2}", "block_id1": f"{canvas.global_id+3}"}),
                    ]
            else:
                if y+height==canvas.height:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x, y]}),
                        Move("lcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2", "orientation": "vertical", "offset": x+width}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.2.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+2}", "block_id1": f"{canvas.global_id+3}"}),
                    ]
                else:
                    return [
                        Move("pcut", {"block_id": canvas.coord_to_block_id[y][x], "point": [x, y]}),
                        Move("pcut", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2", "point": [x+width, y+height]}),
                        Move("color", {"block_id": f"{canvas.coord_to_block_id[y][x]}.2.0", "color": color}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.2.1"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.2.2", "block_id1": f"{canvas.coord_to_block_id[y][x]}.2.3"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+1}", "block_id1": f"{canvas.global_id+2}"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+3}", "block_id1": f"{canvas.coord_to_block_id[y][x]}.3"}),
                        Move("merge", {"block_id0": f"{canvas.coord_to_block_id[y][x]}.0", "block_id1": f"{canvas.coord_to_block_id[y][x]}.1"}),
                        Move("merge", {"block_id0": f"{canvas.global_id+4}", "block_id1": f"{canvas.global_id+5}"}),
                    ]

# canvas = Canvas(400, 400)
# target_image = cv2.imread("./1.png", cv2.IMREAD_UNCHANGED)
# target_image = target_image[::-1, :, :]
# target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)
# (cand_rect, cand_score_diff) = find_cand_rect(canvas, target_image)
# print(cand_rect, cand_score_diff)
# ((x, y, width, height), (r, g, b, a)) = cand_rect
# canvas.pixels[y:y+height, x:x+width] = [r, g, b, a]
# while True:
    # (cand_rect, cand_score_diff) = find_cand_rect(canvas, target_image)
    # print(cand_rect, cand_score_diff)
    # if cand_score_diff<0:
        # ((x, y, width, height), (r, g, b, a)) = cand_rect
        # canvas.pixels[y:y+height, x:x+width] = [r, g, b, a]
    # else:
        # break

# print(cand_rect, cand_score_diff)
# cv2.imwrite("./ann.png", cv2.cvtColor(canvas.pixels[::-1].astype(np.uint8), cv2.COLOR_BGRA2RGBA))
# cv2.waitKey(0)
