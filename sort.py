def quick_sort(A):
    if len(A) <= 1:
        return
    barrier = A[0]['new']
    L, R, M = [], [], []
    for x in A:
        if x['new'] < barrier:
            L.append(x)
        elif x['new'] == barrier:
            M.append(x)
        else:
            R.append(x)
    quick_sort(L)
    quick_sort(R)
    k = 0
    for x in L+M+R:
        A[k] = x
        k += 1
