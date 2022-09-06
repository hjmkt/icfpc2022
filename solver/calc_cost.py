from common import *
from util import *
from icfpc2022_api import *


def calc_cost(x, y, width, height, alternative_cost=False):
    cut_cost = 0
    pcut_alpha = 3 if alternative_cost else 10
    lcut_alpha = 2 if alternative_cost else 7

    # (x,y)でpcut
    cut_cost += pcut_alpha

    # (x+width, y+height)でpcut
    cut_cost += round(pcut_alpha * 400 * 400 / ((400 - x) * (400 - y)))
    color_cost = round(5 * 400 * 400 / (width * height))

    # [x:400,y:400]をmerge

    a, b, c, d = 400 - y - height, height, width, 400 - x - width

    merge1 = 0  # 先に横のmergeをする場合

    merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
    merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
    merge1 += round(400 * 400 / (max(a, b) * (c + d)))  # [x:400,y:400]をmerge

    merge2 = 0  # 先に縦のmergeをする場合

    merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
    merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
    merge2 += round(400 * 400 / (max(c, d) * (a + b)))  # [x:400,y:400]をmerge

    if merge1 < merge2:
        merge_flag1 = 1  # 先に横をmergeする場合は1
    else:
        merge_flag1 = 0

    # 全体をmerge

    a, b, c, d = 400 - y, y, x, 400 - x

    merge3 = 0  # 先に横のmergeをする場合

    merge3 += round(400 * 400 / (a * max(c, d)))  # 上の部分
    merge3 += round(400 * 400 / (b * max(c, d)))  # 下の部分
    merge3 += round(400 * 400 / (max(a, b) * (c + d)))  # [x:400,y:400]をmerge

    merge4 = 0  # 先に縦のmergeをする場合

    merge4 += round(400 * 400 / (max(a, b) * c))  # 左の部分
    merge4 += round(400 * 400 / (max(a, b) * d))  # 右の部分
    merge4 += round(400 * 400 / (max(c, d) * (a + b)))  # [x:400,y:400]をmerge

    if merge3 < merge4:
        merge_flag2 = 1  # 先に横をmergeする場合は1
    else:
        merge_flag2 = 0

    costsum = cut_cost + color_cost + min(merge1, merge2) + min(merge3, merge4)

    # print(cut_cost,color_cost,merge1,merge2,merge3,merge4,costsum)

    return costsum, merge_flag1, merge_flag2


def cost_calc_fin(x, y, width, height, alternative_cost=False):
    pcut_alpha = 3 if alternative_cost else 10
    lcut_alpha = 2 if alternative_cost else 7
    if x == 0:
        if x + width == 400:
            if y == 0:
                if y + height == 400:
                    return 5, -1, -1, -1
                else:
                    cut_cost = lcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))
                    mergecost = round(400 * 400 / (400 * max(height, 400 - height)))

                    return cut_cost + color_cost + mergecost, -1, -1, -1
            else:
                if y + height == 400:
                    cut_cost = lcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))
                    mergecost = round(400 * 400 / (400 * max(height, 400 - height)))

                    return cut_cost + color_cost + mergecost, -1, -1, -1
                else:
                    if y + height > 400 - y:  # 上からcut, 下からmerge
                        cut_cost = lcut_alpha + round(lcut_alpha * 400 / (y + height))
                        color_cost = round(5 * 400 * 400 / (width * height))
                        mergecost = round(
                            1 * 400 * 400 / (width * max(y, height))
                        ) + round(
                            1 * 400 * 400 / (width * max(y + height, 400 - y - height))
                        )

                        return cut_cost + color_cost + mergecost, -1, -1, -1

                    else:  # 下からcut, 上からmerge
                        cut_cost = lcut_alpha + round(lcut_alpha * 400 / (400 - y))
                        color_cost = round(5 * 400 * 400 / (width * height))
                        mergecost = round(
                            1 * 400 * 400 / (width * max(400 - y - height, height))
                        ) + round(1 * 400 * 400 / (width * max(y, 400 - y)))

                        return cut_cost + color_cost + mergecost, -1, -1, -1
        else:
            if y == 0:
                if y + height == 400:
                    cut_cost = lcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))
                    mergecost = round(400 * 400 / (400 * max(width, 400 - width)))

                    return cut_cost + color_cost + mergecost, -1, -1, -1

                else:
                    cut_cost = pcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))

                    a, b, c, d = 400 - height, height, width, 400 - width

                    merge1 = 0  # 先に横のmergeをする場合

                    merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                    merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                    merge1 += round(
                        400 * 400 / (max(a, b) * (c + d))
                    )  # [x:400,y:400]をmerge

                    merge2 = 0  # 先に縦のmergeをする場合

                    merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                    merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                    merge2 += round(
                        400 * 400 / (max(c, d) * (a + b))
                    )  # [x:400,y:400]をmerge

                    if merge1 < merge2:
                        merge_flag1 = 1  # 先に横をmergeする場合は1
                    else:
                        merge_flag1 = 0

                    mergecost = min(merge1, merge2)

                    return cut_cost + color_cost + mergecost, -1, merge_flag1, -1
            else:
                if y + height == 400:
                    cut_cost = pcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))

                    a, b, c, d = 400 - height, height, width, 400 - width

                    merge1 = 0  # 先に横のmergeをする場合

                    merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                    merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                    merge1 += round(
                        400 * 400 / (max(a, b) * (c + d))
                    )  # [x:400,y:400]をmerge

                    merge2 = 0  # 先に縦のmergeをする場合

                    merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                    merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                    merge2 += round(
                        400 * 400 / (max(c, d) * (a + b))
                    )  # [x:400,y:400]をmerge

                    if merge1 < merge2:
                        merge_flag1 = 1  # 先に横をmergeする場合は1
                    else:
                        merge_flag1 = 0

                    mergecost = min(merge1, merge2)

                    return cut_cost + color_cost + mergecost, -1, merge_flag1, -1

                else:
                    # pcutした後にlcutするパターン
                    if y + height > 400 - y:  # 上をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (width * (y + height))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(400 * 400 / (width * max(y, height)))
                        a, b, c, d = 400 - y - height, y + height, width, 400 - width

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1

                    else:  # 下をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (width * (400 - y))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(
                            400 * 400 / (width * max(400 - y - height, height))
                        )
                        a, b, c, d = 400 - y, y, width, 400 - width

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1

    else:
        if x + width == 400:
            if y == 0:
                if y + height == 400:
                    cut_cost = lcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))
                    mergecost = round(400 * 400 / (400 * max(width, 400 - width)))

                    return cut_cost + color_cost + mergecost, -1, -1, -1
                else:
                    cut_cost = pcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))

                    a, b, c, d = 400 - height, height, width, 400 - width

                    merge1 = 0  # 先に横のmergeをする場合

                    merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                    merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                    merge1 += round(
                        400 * 400 / (max(a, b) * (c + d))
                    )  # [x:400,y:400]をmerge

                    merge2 = 0  # 先に縦のmergeをする場合

                    merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                    merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                    merge2 += round(
                        400 * 400 / (max(c, d) * (a + b))
                    )  # [x:400,y:400]をmerge

                    if merge1 < merge2:
                        merge_flag1 = 1  # 先に横をmergeする場合は1
                    else:
                        merge_flag1 = 0

                    mergecost = min(merge1, merge2)

                    return cut_cost + color_cost + mergecost, -1, merge_flag1, -1
            else:
                if y + height == 400:
                    cut_cost = pcut_alpha
                    color_cost = round(5 * 400 * 400 / (width * height))

                    a, b, c, d = 400 - height, height, width, 400 - width

                    merge1 = 0  # 先に横のmergeをする場合

                    merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                    merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                    merge1 += round(
                        400 * 400 / (max(a, b) * (c + d))
                    )  # [x:400,y:400]をmerge

                    merge2 = 0  # 先に縦のmergeをする場合

                    merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                    merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                    merge2 += round(
                        400 * 400 / (max(c, d) * (a + b))
                    )  # [x:400,y:400]をmerge

                    if merge1 < merge2:
                        merge_flag1 = 1  # 先に横をmergeする場合は1
                    else:
                        merge_flag1 = 0

                    mergecost = min(merge1, merge2)

                    return cut_cost + color_cost + mergecost, -1, merge_flag1, -1
                else:
                    # pcutした後にlcutするパターン
                    if y + height > 400 - y:  # 上をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (width * (y + height))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(400 * 400 / (width * max(y, height)))
                        a, b, c, d = 400 - y - height, y + height, width, 400 - width

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1

                    else:  # 下をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (width * (400 - y))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(
                            400 * 400 / (width * max(400 - y - height, height))
                        )
                        a, b, c, d = 400 - y, y, width, 400 - width

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1
        else:
            if y == 0:
                if y + height == 400:
                    if x + width > 400 - x:  # 右からcut, 左からmerge
                        cut_cost = lcut_alpha + round(
                            lcut_alpha * 400 * 400 / (x + width)
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))
                        mergecost = round(
                            1 * 400 * 400 / (height * max(x, width))
                        ) + round(
                            1 * 400 * 400 / (height * max(x + width, 400 - x - width))
                        )

                        return cut_cost + color_cost + mergecost, -1, -1, -1

                    else:  # 左からcut, 右からmerge
                        cut_cost = lcut_alpha + round(lcut_alpha * 400 / (400 - x))
                        color_cost = round(5 * 400 * 400 / (width * height))
                        mergecost = round(
                            1 * 400 * 400 / (height * max(400 - x - width, width))
                        ) + round(1 * 400 * 400 / (height * max(x, 400 - x)))

                        return cut_cost + color_cost + mergecost, -1, -1, -1
                else:
                    # pcutした後にlcutするパターン
                    if x + width > 400 - x:  # 右をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (height * (x + width))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(400 * 400 / (height * max(x, width)))
                        a, b, c, d = 400 - height, height, x + width, 400 - width - x

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1

                    else:  # 左をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (height * (400 - x))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(
                            400 * 400 / (height * max(400 - x - width, width))
                        )
                        a, b, c, d = 400 - height, height, 400 - x, x

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1
            else:
                if y + height == 400:
                    # pcutした後にlcutするパターン
                    if x + width > 400 - x:  # 右をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (height * (x + width))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(400 * 400 / (height * max(x, width)))
                        a, b, c, d = 400 - y, y, x + width, 400 - width - x

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1

                    else:  # 左をpcut
                        cut_cost = pcut_alpha + round(
                            lcut_alpha * 400 * 400 / (height * (400 - x))
                        )
                        color_cost = round(5 * 400 * 400 / (width * height))

                        merge0 = round(
                            400 * 400 / (height * max(400 - x - width, width))
                        )
                        a, b, c, d = 400 - y, y, 400 - x, x

                        merge1 = 0  # 先に横のmergeをする場合

                        merge1 += round(400 * 400 / (a * max(c, d)))  # 上の部分
                        merge1 += round(400 * 400 / (b * max(c, d)))  # 下の部分
                        merge1 += round(
                            400 * 400 / (max(a, b) * (c + d))
                        )  # [x:400,y:400]をmerge

                        merge2 = 0  # 先に縦のmergeをする場合

                        merge2 += round(400 * 400 / (max(a, b) * c))  # 左の部分
                        merge2 += round(400 * 400 / (max(a, b) * d))  # 右の部分
                        merge2 += round(
                            400 * 400 / (max(c, d) * (a + b))
                        )  # [x:400,y:400]をmerge

                        if merge1 < merge2:
                            merge_flag1 = 1  # 先に横をmergeする場合は1
                        else:
                            merge_flag1 = 0

                        mergecost = merge0 + min(merge1, merge2)

                        return cut_cost + color_cost + mergecost, -1, merge_flag1, -1
                else:
                    costmin = 1e9
                    hflag = 0
                    m1flag = 0
                    m2flag = 0

                    # そのまま
                    costsum, merge_flag, merge_flag2 = calc_cost(
                        x, y, width, height, alternative_cost
                    )

                    if costmin > costsum:
                        costmin = costsum
                        hflag = 0
                        m1flag = merge_flag
                        m2flag = merge_flag2

                    # 左右反転
                    costsum, merge_flag, merge_flag2 = calc_cost(
                        400 - x - width, y, width, height, alternative_cost
                    )

                    if costmin > costsum:
                        costmin = costsum
                        hflag = 1
                        m1flag = merge_flag
                        m2flag = merge_flag2

                    # 上下反転
                    costsum, merge_flag, merge_flag2 = calc_cost(
                        x, 400 - y - height, width, height, alternative_cost
                    )

                    if costmin > costsum:
                        costmin = costsum
                        hflag = 2
                        m1flag = merge_flag
                        m2flag = merge_flag2

                    # 上下左右反転
                    costsum, merge_flag, merge_flag2 = calc_cost(
                        400 - x - width,
                        400 - y - height,
                        width,
                        height,
                        alternative_cost,
                    )

                    if costmin > costsum:
                        costmin = costsum
                        hflag = 3
                        m1flag = merge_flag
                        m2flag = merge_flag2

                    return costmin, hflag, m1flag, m2flag


def change_hmflag_to_move(
    block_init_id, x, y, width, height, color, hflag, m1flag, m2flag
):
    if x == 0:
        if x + width == 400:
            if y == 0:
                if y + height == 400:
                    return [
                        Move("color", {"block_id": f"{block_init_id}", "color": color}),
                    ]
                else:
                    return [
                        Move(
                            "lcut",
                            {
                                "block_id": f"{block_init_id}",
                                "orientation": "horizontal",
                                "offset": y + height,
                            },
                        ),
                        Move(
                            "color", {"block_id": f"{block_init_id}.0", "color": color}
                        ),
                        Move(
                            "merge",
                            {
                                "block_id0": f"{block_init_id}.0",
                                "block_id1": f"{block_init_id}.1",
                            },
                        ),
                    ]
            else:
                if y + height == 400:
                    return [
                        Move(
                            "lcut",
                            {
                                "block_id": f"{block_init_id}",
                                "orientation": "horizontal",
                                "offset": y,
                            },
                        ),
                        Move(
                            "color", {"block_id": f"{block_init_id}.1", "color": color}
                        ),
                        Move(
                            "merge",
                            {
                                "block_id0": f"{block_init_id}.0",
                                "block_id1": f"{block_init_id}.1",
                            },
                        ),
                    ]
                else:
                    if y + height > 400 - y:
                        return [
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "orientation": "horizontal",
                                    "offset": y + height,
                                },
                            ),
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}.0",
                                    "orientation": "horizontal",
                                    "offset": y,
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.0.1", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0.0",
                                    "block_id1": f"{block_init_id}.0.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id}.1",
                                },
                            ),
                        ]
                    else:
                        return [
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "orientation": "horizontal",
                                    "offset": y,
                                },
                            ),
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}.1",
                                    "orientation": "horizontal",
                                    "offset": y + height,
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.1.0", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.1.0",
                                    "block_id1": f"{block_init_id}.1.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id}.0",
                                },
                            ),
                        ]
        else:
            if y == 0:
                if y + height == 400:
                    return [
                        Move(
                            "lcut",
                            {
                                "block_id": f"{block_init_id}",
                                "orientation": "vertical",
                                "offset": x + width,
                            },
                        ),
                        Move(
                            "color", {"block_id": f"{block_init_id}.0", "color": color}
                        ),
                        Move(
                            "merge",
                            {
                                "block_id0": f"{block_init_id}.0",
                                "block_id1": f"{block_init_id}.1",
                            },
                        ),
                    ]
                else:
                    if m1flag == 1:
                        return [
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x + width, y + height],
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.0", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.2",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]
                    else:
                        return [
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x + width, y + height],
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.0", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.1",
                                    "block_id1": f"{block_init_id}.2",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]

            else:
                if y + height == 400:
                    if m1flag == 1:
                        return [
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x + width, y],
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.3", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.2",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]
                    else:
                        return [
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x + width, y],
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.3", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.1",
                                    "block_id1": f"{block_init_id}.2",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]

                else:
                    if y + height > 400 - y:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.0",
                                        "orientation": "horizontal",
                                        "offset": y,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.0.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.0",
                                        "block_id1": f"{block_init_id}.0.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.0",
                                        "orientation": "horizontal",
                                        "offset": y,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.0.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.0",
                                        "block_id1": f"{block_init_id}.0.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                    else:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.3",
                                        "orientation": "horizontal",
                                        "offset": y + height,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.3.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.0",
                                        "block_id1": f"{block_init_id}.3.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.3",
                                        "orientation": "horizontal",
                                        "offset": y + height,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.3.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.0",
                                        "block_id1": f"{block_init_id}.3.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.0",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]

    else:
        if x + width == 400:
            if y == 0:
                if y + height == 400:
                    return [
                        Move(
                            "lcut",
                            {
                                "block_id": f"{block_init_id}",
                                "orientation": "vertical",
                                "offset": x,
                            },
                        ),
                        Move(
                            "color", {"block_id": f"{block_init_id}.1", "color": color}
                        ),
                        Move(
                            "merge",
                            {
                                "block_id0": f"{block_init_id}.0",
                                "block_id1": f"{block_init_id}.1",
                            },
                        ),
                    ]
                else:
                    if m1flag == 1:
                        return [
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x, y + height],
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.1", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.2",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]
                    else:
                        return [
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x, y + height],
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.1", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.1",
                                    "block_id1": f"{block_init_id}.2",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]

            else:
                if y + height == 400:
                    if m1flag == 1:
                        return [
                            Move(
                                "pcut",
                                {"block_id": f"{block_init_id}", "point": [x, y]},
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.2", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.2",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]
                    else:
                        return [
                            Move(
                                "pcut",
                                {"block_id": f"{block_init_id}", "point": [x, y]},
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.2", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0",
                                    "block_id1": f"{block_init_id}.3",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.1",
                                    "block_id1": f"{block_init_id}.2",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id+2}",
                                },
                            ),
                        ]

                else:
                    if y + height > 400 - y:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.1",
                                        "orientation": "horizontal",
                                        "offset": y,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.1.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.0",
                                        "block_id1": f"{block_init_id}.1.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.0",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.1",
                                        "orientation": "horizontal",
                                        "offset": y,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.1.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.0",
                                        "block_id1": f"{block_init_id}.1.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                    else:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {"block_id": f"{block_init_id}", "point": [x, y]},
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.2",
                                        "orientation": "horizontal",
                                        "offset": y + height,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.2.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.0",
                                        "block_id1": f"{block_init_id}.2.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {"block_id": f"{block_init_id}", "point": [x, y]},
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.2",
                                        "orientation": "horizontal",
                                        "offset": y + height,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.2.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.0",
                                        "block_id1": f"{block_init_id}.2.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
        else:
            if y == 0:
                if y + height == 400:
                    if x + width > 400 - x:  # 右からcut, 左からmerge
                        return [
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "orientation": "vertical",
                                    "offset": x + width,
                                },
                            ),
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}.0",
                                    "orientation": "vertical",
                                    "offset": x,
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.0.1", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.0.0",
                                    "block_id1": f"{block_init_id}.0.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id}.1",
                                },
                            ),
                        ]
                    else:
                        return [
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "orientation": "vertical",
                                    "offset": x,
                                },
                            ),
                            Move(
                                "lcut",
                                {
                                    "block_id": f"{block_init_id}.1",
                                    "orientation": "vertical",
                                    "offset": x + width,
                                },
                            ),
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.1.0", "color": color},
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id}.1.0",
                                    "block_id1": f"{block_init_id}.1.1",
                                },
                            ),
                            Move(
                                "merge",
                                {
                                    "block_id0": f"{block_init_id+1}",
                                    "block_id1": f"{block_init_id}.0",
                                },
                            ),
                        ]

                else:
                    if x + width > 400 - x:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.0",
                                        "orientation": "vertical",
                                        "offset": x,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.0.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.0",
                                        "block_id1": f"{block_init_id}.0.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.0",
                                        "orientation": "vertical",
                                        "offset": x,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.0.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.0",
                                        "block_id1": f"{block_init_id}.0.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                    else:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.1",
                                        "orientation": "vertical",
                                        "offset": x + width,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.1.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.0",
                                        "block_id1": f"{block_init_id}.1.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.0",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x, y + height],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.1",
                                        "orientation": "vertical",
                                        "offset": x + width,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.1.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.0",
                                        "block_id1": f"{block_init_id}.1.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
            else:
                if y + height == 400:
                    if x + width > 400 - x:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.3",
                                        "orientation": "vertical",
                                        "offset": x,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.3.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.0",
                                        "block_id1": f"{block_init_id}.3.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {
                                        "block_id": f"{block_init_id}",
                                        "point": [x + width, y],
                                    },
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.3",
                                        "orientation": "vertical",
                                        "offset": x,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.3.1",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.0",
                                        "block_id1": f"{block_init_id}.3.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.0",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                    else:
                        if m1flag == 1:
                            return [
                                Move(
                                    "pcut",
                                    {"block_id": f"{block_init_id}", "point": [x, y]},
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.2",
                                        "orientation": "vertical",
                                        "offset": x + width,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.2.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.0",
                                        "block_id1": f"{block_init_id}.2.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                        else:
                            return [
                                Move(
                                    "pcut",
                                    {"block_id": f"{block_init_id}", "point": [x, y]},
                                ),
                                Move(
                                    "lcut",
                                    {
                                        "block_id": f"{block_init_id}.2",
                                        "orientation": "vertical",
                                        "offset": x + width,
                                    },
                                ),
                                Move(
                                    "color",
                                    {
                                        "block_id": f"{block_init_id}.2.0",
                                        "color": color,
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.0",
                                        "block_id1": f"{block_init_id}.2.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                ),
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+2}",
                                        "block_id1": f"{block_init_id+3}",
                                    },
                                ),
                            ]
                else:
                    MOVES = []

                    if hflag == 0:
                        MOVES.append(
                            Move(
                                "pcut",
                                {"block_id": f"{block_init_id}", "point": [x, y]},
                            )
                        )
                        MOVES.append(
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}.2",
                                    "point": [x + width, y + height],
                                },
                            )
                        )
                        MOVES.append(
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.2.0", "color": color},
                            )
                        )

                        # 小さい長方形のmerge

                        if m1flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.0",
                                        "block_id1": f"{block_init_id}.2.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.2",
                                        "block_id1": f"{block_init_id}.2.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.0",
                                        "block_id1": f"{block_init_id}.2.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2.1",
                                        "block_id1": f"{block_init_id}.2.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        # 全体のmerge

                        if m2flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                    elif hflag == 1:
                        MOVES.append(
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x + width, y],
                                },
                            )
                        )
                        MOVES.append(
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}.3",
                                    "point": [x, y + height],
                                },
                            )
                        )
                        MOVES.append(
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.3.1", "color": color},
                            )
                        )

                        # 小さい長方形のmerge

                        if m1flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.0",
                                        "block_id1": f"{block_init_id}.3.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.2",
                                        "block_id1": f"{block_init_id}.3.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.0",
                                        "block_id1": f"{block_init_id}.3.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.3.1",
                                        "block_id1": f"{block_init_id}.3.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        # 全体のmerge

                        if m2flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.0",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                    elif hflag == 2:
                        MOVES.append(
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x, y + height],
                                },
                            )
                        )
                        MOVES.append(
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}.1",
                                    "point": [x + width, y],
                                },
                            )
                        )
                        MOVES.append(
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.1.3", "color": color},
                            )
                        )

                        # 小さい長方形のmerge

                        if m1flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.0",
                                        "block_id1": f"{block_init_id}.1.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.2",
                                        "block_id1": f"{block_init_id}.1.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.0",
                                        "block_id1": f"{block_init_id}.1.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1.1",
                                        "block_id1": f"{block_init_id}.1.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        # 全体のmerge

                        if m2flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.0",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                    else:
                        MOVES.append(
                            Move(
                                "pcut",
                                {
                                    "block_id": f"{block_init_id}",
                                    "point": [x + width, y + height],
                                },
                            )
                        )
                        MOVES.append(
                            Move(
                                "pcut",
                                {"block_id": f"{block_init_id}.0", "point": [x, y]},
                            )
                        )
                        MOVES.append(
                            Move(
                                "color",
                                {"block_id": f"{block_init_id}.0.2", "color": color},
                            )
                        )

                        # 小さい長方形のmerge

                        if m1flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.0",
                                        "block_id1": f"{block_init_id}.0.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.2",
                                        "block_id1": f"{block_init_id}.0.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.0",
                                        "block_id1": f"{block_init_id}.0.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.0.1",
                                        "block_id1": f"{block_init_id}.0.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+1}",
                                        "block_id1": f"{block_init_id+2}",
                                    },
                                )
                            )

                        # 全体のmerge

                        if m2flag == 1:  # 先に横をmergeする場合は1
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.1",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.2",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                        else:
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+3}",
                                        "block_id1": f"{block_init_id}.3",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id}.1",
                                        "block_id1": f"{block_init_id}.2",
                                    },
                                )
                            )
                            MOVES.append(
                                Move(
                                    "merge",
                                    {
                                        "block_id0": f"{block_init_id+4}",
                                        "block_id1": f"{block_init_id+5}",
                                    },
                                )
                            )

                    return MOVES
