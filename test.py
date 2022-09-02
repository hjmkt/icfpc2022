from common import *
import cv2

canvas = Canvas(400, 400)

moves = [
    Move("lcut", {"block_id": "0", "orientation": "horizontal", "offset": 342}),
    Move("lcut", {"block_id": "0.0", "orientation": "horizontal", "offset": 124}),
    Move("lcut", {"block_id": "0.0.0", "orientation": "horizontal", "offset": 65}),
    Move("color", {"block_id": "0.0.0.1", "color": [226, 227, 225, 255]}),
    Move("color", {"block_id": "0.0.1", "color": [91, 91, 85, 255]}),
    Move("color", {"block_id": "0.1", "color": [7, 148, 182, 255]}),
]

target_image = cv2.imread("./6.png", cv2.IMREAD_UNCHANGED)
target_image = target_image[::-1, :, :]
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)
# print(target_image.shape)

# similarity = canvas.compute_similarity(target_image)
# print(f"similarity = {similarity}")
# cv2.imshow("pre", canvas.pixels.astype(np.uint8))
# cv2.waitKey(0)

for move in moves:
    canvas.exec_move(move)


cost = canvas.get_current_cost()
similarity = canvas.compute_similarity(target_image)
score = canvas.compute_score(target_image)
print(f"cost = {cost}")
print(f"similarity = {similarity}")
print(f"score = {score}")
# cv2.imshow("post", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
# cv2.imwrite("post.png", cv2.cvtColor(canvas.pixels.astype(np.uint8)[::-1, :, :], cv2.COLOR_BGRA2RGBA))
# cv2.waitKey(0)
