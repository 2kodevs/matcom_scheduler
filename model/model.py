from model.utils import *

def distance(data1:list, data2:list):
    '''
    Return the number of iversions
    necessary to transform data1 in data2
    <param> data1 - list of data
    <param> data2 - list of data
    <return> int - Number of inversions
    '''
    d, n = {}, 0

    order1, order2 = data1.copy(), data2.copy()
    order1.sort()
    order2.sort()
    just_one = len(data1) > 0
    for i in range(1, len(order1)):
        if order1[i] == order1[i - 1]:
            just_one = False
            break

    if order1 != order2 or not just_one:
        # //TODO: raise an error
        print("malformed args")
        return -1

    def update(item, n):
        pos = d.get(item)
        if pos is None:
            pos = n
            d[item] = n
            n += 1
        return n

    for item in data1: n = update(item, n)
    for item in data2: n = update(item, n)
    
    idx = [0] * (n + 1) 
    for (i, item) in enumerate(data1):
        idx[d[item]] = i
    inv = 0
    for (i, item) in enumerate(data2):
        inv += abs(i - idx[d[item]])

    return inv

def solve(data):
    '''
    Given a data set of option
    find the distribution that
    minimice the sumatory of 
    inversions with every option
    '''
    if not data:
        return None
    dis = len(data) ** 2
    best = data[0].copy()
    best.sort()
    cur = best.copy()
    while True:
        sum = 0
        for item in data:
            d = distance(item, cur)
            # //TODO: Manage the malformed args error
            if d == -1: 
                return None
            sum += d
        if sum < dis:
            dis, best = sum, cur.copy()
        if not next_permutation(cur):
            break
    return best

