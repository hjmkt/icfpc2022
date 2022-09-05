from common import *
import json
from isl_json_reader import *
from common import *
from util import *
from icfpc2022_api import *
import cv2
import sys
import time
from rect_fill import *
import argparse
from calc_cost import *
from solve_with_rect_fill import solve

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--problem", type=int)
parser.add_argument("-s", "--seed", type=int)
# parser.add_argument("-m", "--merge", type=int)
parser.add_argument("-t", "--token", type=str)
parser.add_argument("-r", "--resume", type=str)
args = parser.parse_args()

isl_json_path= args.resume
MOVES=read_json(isl_json_path)
RECT=[]

target_image = cv2.imread(f"./{args.problem}.png", cv2.IMREAD_UNCHANGED)
target_image = target_image[::-1, :, :]
target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)

canvas = Canvas(400, 400)

for move in MOVES:
    if move.move_type=="color":
        block_id = move.options["block_id"]
        color = move.options["color"]
        block = canvas.blocks[block_id]

        RECT.append([block.x,block.y,block.width,block.height,color])

    canvas.exec_move(move)

best_score=canvas.compute_score(target_image)

def calc_rect_score(RECT)  :
    canvas2 = Canvas(400, 400)
    MOVES2=[]
    
    for x,y,width,height,color in RECT:
        costmin,hflag,m1flag,m2flag=cost_calc_fin(x,y,width,height)
        moves=change_hmflag_to_move(canvas2.global_id,x,y,width,height,color,hflag,m1flag,m2flag)
        MOVES2+=moves
        for m in moves:
            canvas2.exec_move(m)

    return canvas2.compute_score(target_image)

# スコア計算せずに削れるコストを削る

USED=[0]*(400*400)

for ind in range(len(RECT)-1,-1,-1):
    print(ind)

    while RECT[ind][0]>0:
        x,y,width,height,_=RECT[ind]
        flag=1
        for j in range(y,y+height):
            if USED[(x-1)*400+j]==0:
                flag=0
                break
        if flag==1:
            RECT[ind][0]-=1
            RECT[ind][2]+=1
        else:
            break

    while RECT[ind][1]>0:
        x,y,width,height,_=RECT[ind]
        flag=1
        for i in range(x,x+width):
            if USED[i*400+y-1]==0:
                flag=0
                break
        if flag==1:
            RECT[ind][1]-=1
            RECT[ind][3]+=1
        else:
            break

    while RECT[ind][0]+RECT[ind][2]<400:
        x,y,width,height,_=RECT[ind]
        flag=1
        for j in range(y,y+height):
            if USED[(x+width)*400+j]==0:
                flag=0
                break
        if flag==1:
            RECT[ind][2]+=1
        else:
            break

    while RECT[ind][1]+RECT[ind][3]<400:
        x,y,width,height,_=RECT[ind]
        flag=1
        for i in range(x,x+width):
            if USED[i*400+y+height]==0:
                flag=0
                break
        if flag==1:
            RECT[ind][3]+=1
        else:
            break

    x,y,width,height,_=RECT[ind]

    for i in range(x,x+width):
        for j in range(y,y+height):
            USED[i*400+j]=1        

# ここから、スコア計算をして削る

best_score=calc_rect_score(RECT)

for i in range(len(RECT)-1,-1,-1):
    x,y,width,height,color=RECT[i]

    f0=f1=f2=f3=1

    while True:
        print(i,len(RECT),best_score)
        if x>0 and f0==1:
            RECT[i][0]-=1
            RECT[i][2]+=1
            x-=1
            width+=1
                    
            sc=calc_rect_score(RECT)
            if sc<=best_score:
                best_score=sc
                continue
            else:
                RECT[i][0]+=1
                RECT[i][2]-=1
                x+=1
                width-=1
                f0=0

        if y>0 and f1==1:
            RECT[i][1]-=1
            RECT[i][3]+=1
            y-=1
            height+=1            

            sc=calc_rect_score(RECT)
            if sc<=best_score:
                best_score=sc
                continue
            else:
                RECT[i][1]+=1
                RECT[i][3]-=1
                y+=1
                height-=1
                f1=0

        if x+width<400 and f2==1:
            RECT[i][2]+=1
            width+=1

            sc=calc_rect_score(RECT)
            if sc<=best_score:
                best_score=sc
                continue
            else:
                RECT[i][2]-=1
                width-=1
                f2=0

        if y+height<400 and f3==1:
            RECT[i][3]+=1
            height+=1

            sc=calc_rect_score(RECT)
            if sc<=best_score:
                best_score=sc
                continue
            else:
                RECT[i][3]-=1
                height-=1
                f3=0
        break

canvas2 = Canvas(400, 400)
MOVES2=[]
for x,y,width,height,color in RECT:
    costmin,hflag,m1flag,m2flag=cost_calc_fin(x,y,width,height)
    moves=change_hmflag_to_move(canvas2.global_id,x,y,width,height,color,hflag,m1flag,m2flag)
    MOVES2+=moves
    for m in moves:
        canvas2.exec_move(m)

while MOVES2[-1].move_type=="merge":
    MOVES2.pop()

score = canvas2.compute_score(target_image)
isl = moves_to_isl(MOVES2)
isl_path = f"./isl_p{args.problem}_{round(score)}.txt"
with open(isl_path, "w") as f:
    print(isl, file=f)

solve(args.problem, args.seed, 0, args.token, MOVES2)
