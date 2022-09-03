from common import *
from util import *
import cv2
import sys
from rect_fill import *

canvas = Canvas(400, 400)

target_image = cv2.imread("./11.png", cv2.IMREAD_UNCHANGED)
target_image = target_image[::-1, :, :]
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)

moves = []
while True:
    (cand_rect, cand_score_diff) = find_cand_rect(canvas, target_image)
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

# for move in moves:
    # canvas.exec_move(move)

cost = canvas.get_current_cost()
similarity = canvas.compute_similarity(target_image)
score = canvas.compute_score(target_image)
print(f"cost = {cost}", file=sys.stderr)
print(f"similarity = {similarity}", file=sys.stderr)
print(f"score = {score}", file=sys.stderr)
# cv2.imshow("post", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
cv2.imwrite("post.png", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
# cv2.waitKey(0)
isl = moves_to_isl(moves)
print(isl)
