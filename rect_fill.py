from common import *
from util import *
import cv2
import numpy as np
from concurrent.futures import ProcessPoolExecutor


def compute_score_diff(canvas, target, rect):
    [[x, y, width, height], [r, g, b, a]] = rect
    current_pixels = canvas.pixels[y:y+height, x:x+width]
    cand_pixels = np.zeros((height, width, 4))
    cand_pixels[:, :] = [r, g, b, a]
    target_pixels = target[y:y+height, x:x+width]
    current_diff = np.sqrt(((target_pixels-current_pixels)**2).sum(axis=-1)).sum() * 0.005
    cand_diff = np.sqrt(((target_pixels-cand_pixels)**2).sum(axis=-1)).sum() * 0.005
    first_rect_size = max((x+width)*(y+height), (canvas.width-x)*(y+height), (x+width)*(canvas.height-y), (canvas.width-x)*(canvas.height-y))
    cost = round(10*0.005) + round(10 * canvas.width * canvas.height / first_rect_size)
    cost += round(5 * canvas.width * canvas.height / width / height * 0.005)
    merge_cost = round(1*0.005) + round(1 * canvas.width * canvas.height / first_rect_size)
    score_diff = cand_diff - current_diff + cost + merge_cost
    return score_diff

def refine(canvas_target_start_rect):
    canvas, target, start_rect = canvas_target_start_rect
    rect = start_rect
    local_best_diff = compute_score_diff(canvas, target, rect)
    for step in [16, 4, 1]:
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
            if tmp_best_diff==0:
                break
            rect[0] = tmp_best_rect[0]
            rect[1] = tmp_best_rect[1]
            if tmp_best_diff<local_best_diff:
                local_best_diff = tmp_best_diff
            else:
                break
    return rect, local_best_diff


def find_cand_rect(canvas, target, num_seeds=16):
    start_rects = [[[np.random.randint(0, canvas.width), np.random.randint(0, canvas.height), 1, 1], np.random.randint(0, 256, (4))] for _ in range(num_seeds)]
    
    best_rect = None
    best_diff = 1e8
    with ProcessPoolExecutor(8) as executor:
        results = executor.map(refine, map(lambda x: (canvas, target, x), start_rects))
    for (local_best_rect, local_best_diff) in results:
        if local_best_diff<best_diff:
            best_diff = local_best_diff
            best_rect = local_best_rect

    return (best_rect, best_diff)

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
