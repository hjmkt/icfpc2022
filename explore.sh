#!/bin/bash

while true; do
    for s in 64 256; do
        for p in `seq 1 25`; do
            for m in 400; do
                count=1
                python3 solve_with_rect_fill.py -p ${p} -m ${m} -s ${s}
                status=$?
                until [[ $? -eq 0 || $count -eq 5 ]]; do
                    python3 solve_with_rect_fill.py -p ${p} -m ${m} -s ${s}
                    status=$?
                    let count=count+1
                done
            done
        done
    done
done
