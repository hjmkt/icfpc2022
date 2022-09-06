from functools import lru_cache
import sys

sys.setrecursionlimit(10**7)


def minimize_cut_cost(CUT_X, CUT_Y):

    line_cut = 7
    point_cut = 10

    FROM = dict()

    @lru_cache(maxsize=None)
    def calc(
        min_x, max_x, min_y, max_y, CUT_X, CUT_Y
    ):  # min_x, min_yは、CUT_X, CUT_Yのindexを与える
        ANS = 1 << 60
        if max_x == min_x + 1 and max_y == min_y + 1:
            return 0

        if max_x > min_x + 1:
            for i in range(min_x + 1, max_x):
                tempscore = (
                    line_cut
                    * 400
                    * 400
                    / (CUT_X[max_x] - CUT_X[min_x])
                    / (CUT_Y[max_y] - CUT_Y[min_y])
                    + calc(min_x, i, min_y, max_y, CUT_X, CUT_Y)
                    + calc(i, max_x, min_y, max_y, CUT_X, CUT_Y)
                )
                if ANS > tempscore:
                    ANS = tempscore
                    FROM[min_x, max_x, min_y, max_y] = (i, -1)

        if max_y > min_y + 1:
            for j in range(min_y + 1, max_y):
                tempscore = (
                    line_cut
                    * 400
                    * 400
                    / (CUT_X[max_x] - CUT_X[min_x])
                    / (CUT_Y[max_y] - CUT_Y[min_y])
                    + calc(min_x, max_x, min_y, j, CUT_X, CUT_Y)
                    + calc(min_x, max_x, j, max_y, CUT_X, CUT_Y)
                )
                if ANS > tempscore:
                    ANS = tempscore
                    FROM[min_x, max_x, min_y, max_y] = (-1, j)

        if max_x > min_x + 1 and max_y > min_y + 1:
            for i in range(min_x + 1, max_x):
                for j in range(min_y + 1, max_y):
                    tempscore = (
                        point_cut
                        * 400
                        * 400
                        / (CUT_X[max_x] - CUT_X[min_x])
                        / (CUT_Y[max_y] - CUT_Y[min_y])
                        + calc(min_x, i, min_y, j, CUT_X, CUT_Y)
                        + calc(min_x, i, j, max_y, CUT_X, CUT_Y)
                        + calc(i, max_x, min_y, j, CUT_X, CUT_Y)
                        + calc(i, max_x, j, max_y, CUT_X, CUT_Y)
                    )
                    if ANS > tempscore:
                        ANS = tempscore
                        FROM[min_x, max_x, min_y, max_y] = (i, j)

        return ANS

    calc(0, len(CUT_X) - 1, 0, len(CUT_Y) - 1, CUT_X, CUT_Y)

    def from_cut(
        block_id, min_x, max_x, min_y, max_y
    ):  # min_x, min_yは、CUT_X, CUT_Yのindexを与える

        if (min_x, max_x, min_y, max_y) in FROM:
            x, y = FROM[min_x, max_x, min_y, max_y]
            if x == -1:
                cut_ans_order.append(
                    "cut" + "[" + block_id + "]" + "[y]" + "[" + str(CUT_Y[y]) + "]"
                )

                Move_type = "lcut"
                options = dict()
                options["block_id"] = block_id
                options["orientation"] = "horizontal"
                options["offset"] = CUT_Y[y]
                cut_ans_order_for_test.append([Move_type, options])

                from_cut(block_id + ".0", min_x, max_x, min_y, y)
                from_cut(block_id + ".1", min_x, max_x, y, max_y)

            elif y == -1:
                cut_ans_order.append(
                    "cut" + "[" + block_id + "]" + "[x]" + "[" + str(CUT_X[x]) + "]"
                )

                Move_type = "lcut"
                options = dict()
                options["block_id"] = block_id
                options["orientation"] = "vertical"
                options["offset"] = CUT_X[x]
                cut_ans_order_for_test.append([Move_type, options])

                from_cut(block_id + ".0", min_x, x, min_y, max_y)
                from_cut(block_id + ".1", x, max_x, min_y, max_y)
            else:
                cut_ans_order.append(
                    "cut"
                    + "["
                    + block_id
                    + "]"
                    + "["
                    + str(CUT_X[x])
                    + ","
                    + str(CUT_Y[y])
                    + "]"
                )

                Move_type = "pcut"
                options = dict()
                options["block_id"] = block_id
                options["point"] = (CUT_X[x], CUT_Y[y])

                cut_ans_order_for_test.append([Move_type, options])

                from_cut(block_id + ".0", min_x, x, min_y, y)
                from_cut(block_id + ".1", x, max_x, min_y, y)

                from_cut(block_id + ".3", min_x, x, y, max_y)
                from_cut(block_id + ".2", x, max_x, y, max_y)

    cut_ans_order = []
    cut_ans_order_for_test = []

    from_cut("0", 0, len(CUT_X) - 1, 0, len(CUT_Y) - 1)

    return cut_ans_order, cut_ans_order_for_test
