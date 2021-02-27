def quick_sort(seq: list):
    if len(seq) <= 1:
        return
    barrier = seq[0]['new']
    L, R, M = [], [], []
    for x in seq:
        if x['new'] < barrier:
            L.append(x)
        elif x['new'] == barrier:
            M.append(x)
        else:
            R.append(x)
    quick_sort(L)
    quick_sort(R)
    k = 0
    for x in L + M + R:
        seq[k] = x
        k += 1
