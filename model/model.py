def distance(data1:list, data2:list):
    '''
    Return the number of iversions
    necessary to transform data1 in data2
    <param> data1 - list of data
    <param> data2 - list of data
    <return> int - Number of inversions
    '''
    d, n, cant = {}, 0, []

    def update(item, n):
        pos = d.get(item)
        if pos is None:
            pos = n
            d[item] = n
            cant.append(0)
            n += 1
        cant[pos] += 1
        return n

    for item in data1: n = update(item, n)
    for item in data2: n = update(item, n)
    
    idx = [0] * (n + 1) 
    for (i, item) in enumerate(data1):
        idx[d[item]] = i
    inv = 0
    for (i, item) in enumerate(data2):
        inv += abs(i - idx[d[item]])

    data1.sort()
    data2.sort()
    if any(x != 2 for x in cant) or data1 != data2 or not data1:
        # //TODO: raise an error
        print("malformed args")
        return -1
    return inv
