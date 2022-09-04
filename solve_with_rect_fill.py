from common import *
from util import *
from icfpc2022_api import *
import cv2
import sys
import time
import copy
import json
from rect_fill import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--problem", type=int)
parser.add_argument("-s", "--seed", type=int)
parser.add_argument("-m", "--merge", type=int)
parser.add_argument("-t", "--token", type=str)
args = parser.parse_args()

width = 400
height = 400


target_image = cv2.imread(f"./{args.problem}.png", cv2.IMREAD_UNCHANGED)
target_image = target_image[::-1, :, :]
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)

canvas = Canvas(width, height)
canvas_for_cost = Canvas(width, height)
global_id = 0

initial_moves = []
if args.problem>=26:
    with open(f"{args.problem}.initial.json") as f:
        initial_config = json.load(f)
        width = initial_config["width"]
        height = initial_config["height"]
        num_blocks = len(initial_config["blocks"])
        if num_blocks==100:
            block_width = 40
            block_height = 40
            rows = 10
            cols = 10
        elif num_blocks==256:
            block_width = 25
            block_height = 25
            rows = 16
            cols = 16
        elif num_blocks==400:
            block_width = 20
            block_height = 20
            rows = 20
            cols = 20
        else:
            block_width = 16
            block_height = 16
            rows = 25
            cols = 25
        for row in range(rows):
            for col in range(cols-1):
                id0 = f"{row*cols}" if col==0 else f"{rows*cols+row*(cols-1)+col-1}"
                id1 = f"{row*cols+col+1}"
                initial_moves.append(Move("merge", {"block_id0": id0, "block_id1": id1}))
        for row in range(rows-1):
            id0 = f"{rows*cols-1+cols-1}" if row==0 else f"{rows*cols-1+rows*(cols-1)+row}"
            id1 = f"{rows*cols-1+(row+2)*(cols-1)}"
            initial_moves.append(Move("merge", {"block_id0": id0, "block_id1": id1}))
        canvas = Canvas(width, height)
        canvas_for_cost = Canvas(width, height)
        global_id = rows*cols - 1
        canvas.global_id = global_id
        canvas_for_cost.global_id = global_id
        for row in range(rows):
            for col in range(cols):
                block = initial_config["blocks"][row*cols+col]
                x0, y0 = block["bottomLeft"]
                x1, y1 = block["topRight"]
                canvas.pixels[y0:y1, x0:x1] = block["color"]
                canvas_for_cost.pixels[y0:y1, x0:x1] = block["color"]
                canvas.blocks[block["blockId"]] = SimpleBlock(x0, y0, x1-x0, y1-y0, block["color"], block["blockId"])
                canvas.all_blocks[block["blockId"]] = SimpleBlock(x0, y0, x1-x0, y1-y0, block["color"], block["blockId"])
                canvas_for_cost.blocks[block["blockId"]] = SimpleBlock(x0, y0, x1-x0, y1-y0, block["color"], block["blockId"])
                canvas_for_cost.all_blocks[block["blockId"]] = SimpleBlock(x0, y0, x1-x0, y1-y0, block["color"], block["blockId"])
                for y in range(y0, y1):
                    for x in range(x0, x1):
                        canvas.coord_to_block_id[y][x] = block["blockId"]
                        canvas_for_cost.coord_to_block_id[y][x] = block["blockId"]
        for move in initial_moves:
            # print(move.move_type, move.options)
            canvas.exec_move(move)

moves = copy.copy(initial_moves)
while True:
    (cand_rect, cand_score_diff) = find_cand_rect(canvas, target_image, args.seed, args.merge)
    print(cand_rect, cand_score_diff, file=sys.stderr)
    rect_moves = rect_to_moves(canvas, cand_rect)
    if cand_score_diff<0 and len(rect_moves)>0:
        for move in rect_moves:
            print(move.move_type, move.options, file=sys.stderr)
            canvas.exec_move(move)
    else:
        break
    moves += rect_moves

while moves[-1].move_type=="merge":
    moves = moves[:-1]

for move in moves:
    canvas_for_cost.exec_move(move)
cost = canvas_for_cost.get_current_cost()
similarity = canvas_for_cost.compute_similarity(target_image)
score = canvas_for_cost.compute_score(target_image)

print(f"cost = {cost}", file=sys.stderr)
print(f"similarity = {similarity}", file=sys.stderr)
print(f"score = {score}", file=sys.stderr)

# cv2.imwrite("post.png", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
isl = moves_to_isl(moves)
isl_path = f"./isl_p{args.problem}_{round(score)}.txt"
with open(isl_path, "w") as f:
    print(isl, file=f)

submission_results = get_results(args.token)
print(submission_results, file=sys.stderr)
retry = 0
while retry<5 and "results" not in submission_results.keys():
    time.sleep(1)
    submission_results = get_results(args.token)
    retry += 1

if retry>=5:
    print("unexpected exit", file=sys.stderr)
    exit()

submission_results = submission_results["results"]
submission_results = list(filter(lambda x: x["problem_id"]==args.problem, submission_results))
if len(submission_results)>0:
    min_score = submission_results[0]["min_cost"]
    if score<min_score:
        print(f"post submission with score = {score}, updated from {min_score}", file=sys.stderr)
        post_submission(args.problem, isl_path, args.token)
    else:
        print(f"score = {score} (min = {min_score})", file=sys.stderr)
else:
    print(f"post submission with score = {score}", file=sys.stderr)
    post_submission(args.problem, isl_path, args.token)
