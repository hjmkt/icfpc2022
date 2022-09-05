from common import *
from minimize_cost_of_rectangle_cut import *
import cv2

CUT_X = (0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400)  # 切りたいx座標
CUT_Y = (0, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400)  # 切りたいy座標

# 切りたいx座標のtuple,y座標のtupleを入力すると、切り方が返ってくる。
cut_ans_order, cut_ans_order_for_test = minimize_cut_cost(CUT_X, CUT_Y)


target_image = cv2.imread("./1.png", cv2.IMREAD_UNCHANGED)
target_image = target_image[::-1, :, :]
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)
# print(target_image.shape)

# similarity = canvas.compute_similarity(target_image)
# print(f"similarity = {similarity}")
# cv2.imshow("pre", canvas.pixels.astype(np.uint8))
# cv2.waitKey(0)

canvas = Canvas(400, 400)

for x, y in cut_ans_order_for_test:
    canvas.exec_move(Move(x, y))


cost = canvas.get_current_cost()
similarity = canvas.compute_similarity(target_image)
score = canvas.compute_score(target_image)
#print(f"cost = {cost}")
#print(f"similarity = {similarity}")
#print(f"score = {score}")
# cv2.imshow("post", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
# cv2.imwrite("post.png", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
# cv2.waitKey(0)

sum_blockpic = dict()
masu_blocks = dict()

for i in range(400):
    for j in range(400):
        bid = canvas.coord_to_block_id[i][j]
        if bid in sum_blockpic:
            masu_blocks[bid] += 1
            sum_blockpic[bid] += target_image[i][j]
        else:
            sum_blockpic[bid] = np.array([0, 0, 0, 0])
            masu_blocks[bid] = 1
            sum_blockpic[bid] += target_image[i][j]


for s in cut_ans_order:
    print(s)

# 各ブロックの色をその平均値にする
for block_id in sum_blockpic:
    C = sum_blockpic[block_id]/masu_blocks[block_id]
    print("color"+"["+str(block_id)+"]"+"["+str(round(C[0]))+"," +
          str(round(C[1]))+","+str(round(C[2]))+","+str(round(C[3]))+"]")
