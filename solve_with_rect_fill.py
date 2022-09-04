from common import *
from util import *
from icfpc2022_api import *
import cv2
import sys
from rect_fill import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--problem", type=int)
parser.add_argument("-s", "--seed", type=int)
parser.add_argument("-m", "--merge", type=int)
parser.add_argument("-t", "--token", type=str)
args = parser.parse_args()

canvas = Canvas(400, 400)

target_image = cv2.imread(f"./{args.problem}.png", cv2.IMREAD_UNCHANGED)
target_image = target_image[::-1, :, :]
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)

moves = []
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

canvas_for_cost = Canvas(400, 400)
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
with open(f"./isl_p{args.problem}_{round(score)}.txt", "w") as f:
    print(isl, file=f)

submission_results = get_results(args.token)["results"]
submission_results = list(filter(lambda x: x["problem_id"]==f"{args.problem}", submission_results))
if len(submission_results)>0:
    min_score = submission_results[0]["min_cost"]
    if score<min_score:
        print(f"post submission with score = {score}, updated from {min_score}", file=sys.stderr)
        post_submission(args.problem, args.token)
else:
    print(f"post submission with score = {score}", file=sys.stderr)
    post_submission(args.problem, args.token)
