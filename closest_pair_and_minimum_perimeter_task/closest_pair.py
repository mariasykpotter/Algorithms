import math


def sort_x(arr):
    arr.sort(key=lambda x: x[0])
    return arr


def sort_y(arr):
    arr.sort(key=lambda x: x[1])
    return arr


def find_distance(tup1, tup2):
    return math.sqrt((tup2[0] - tup1[0]) * (tup2[0] - tup1[0]) + (tup2[1] - tup1[1]) * (tup2[1] - tup1[1]))


def bruteForce(lst, d):
    min = d
    min_tup = ()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if find_distance(lst[i], lst[j]) < min:
                min = find_distance(lst[i], lst[j])
                min_tup = (lst[i], lst[j])
    return min, min_tup


def stripClosest(lst, d):
    min = d
    min_tup = ()
    for i in range(len(lst)):
        j = i + 1
        while j < len(lst) and (lst[j][1] - lst[i][1]) < min:
            if find_distance(lst[i], lst[j]) < min:
                min = find_distance(lst[i], lst[j])
                min_tup = (lst[i], lst[j])
            j += 1
    return min, min_tup


def closestUtil(px, py):
    strip = []
    pyl = []
    pyr = []
    if len(px) <= 3:
        return bruteForce(px, float('inf'))
    else:
        mid = len(px) // 2
        for i in range(1, len(py)):
            if py[i][0] < px[mid][0]:
                pyl.append(py[i])
            else:
                pyr.append(py[i])
        dl = closestUtil(px[:mid + 1], pyl)
        dr = closestUtil(px[mid + 1:], pyr)
        if dl < dr:
            d = dl[0]
            min_tup = dl[1]
        else:
            d = dr[0]
            min_tup = dr[1]
        for i in range(len(py)):
            if (abs(py[i][0] - px[mid][0] < d)):
                strip.append(py[i])
        value = stripClosest(strip, d)
        if value[0] < d:
            return value
        else:
            return d, min_tup


def closest_pair(arr):
    arrx = sort_x(arr)
    arry = sort_y(arr)
    return closestUtil(arrx, arry)


def findPerimeter(tup1, tup2, tup3):
    return find_distance(tup1, tup2) + find_distance(tup1, tup3) + find_distance(tup3, tup2)


def bruteForceP(lst, d):
    min = d
    min_tup = ()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            for k in range(j + 1, len(lst)):
                if findPerimeter(lst[i], lst[j], lst[k]) < min:
                    min = findPerimeter(lst[i], lst[j], lst[k])
                    min_tup = (lst[i], lst[j], lst[k])
    return min, min_tup


def stripMiddle(lst, d):
    min = d
    min_tup = ()
    arrx = sorted(lst, key=lambda x: x[0])
    arry = sorted(lst, key=lambda x: x[1])
    closest = closestUtil(arrx, arry)
    if closest[0] > d:
        return float('inf'), ()
    for el in lst:
        if el not in closest[1]:
            per = findPerimeter(closest[1][0], closest[1][1], el)
            if per < min:
                min = per
                min_tup = (closest[1][0], closest[1][1], el)
    return min, min_tup


def get_longest_side(triangle):
    return max(find_distance(triangle[0], triangle[1]), find_distance(triangle[0], triangle[2]),
               find_distance(triangle[1], triangle[2]))


def perimeterUtil(px):
    strip = []
    pyl = []
    pyr = []
    if len(px) < 3:
        return (float('inf'), ())
    elif len(px) < 6:
        return bruteForceP(px, float('inf'))
    else:
        mid = len(px) // 2
        px_l = px[:mid + 1]
        py_l = sorted(px_l, key=lambda x: x[1])
        px_r = px[mid + 1:]
        py_r = sorted(px_r, key=lambda x: x[1])
        dl = perimeterUtil(px_l)
        dr = perimeterUtil(px_r)
        if dl < dr:
            d = dl[0]
            min_tup = dl[1]
        else:
            d = dr[0]
            min_tup = dr[1]
        longest_edge = get_longest_side(min_tup)
        for i in range(len(py_l)):
            if (abs(py_l[i][0] - px[mid][0]) < longest_edge):
                strip.append(py_l[i])
        for i in range(len(py_r)):
            if (abs(py_r[i][0] - px[mid][0]) < longest_edge):
                strip.append(py_r[i])
        if len(strip) < 3:
            return d, min_tup
        value = stripMiddle(strip, d)
        if value[0] < d:
            return value
        else:
            return d, min_tup


def minimal_perimeter(arr):
    arrx = sorted(arr, key=lambda x: x[0])
    return perimeterUtil(arrx)