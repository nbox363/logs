months = {
    'января': '01',
    'февраля': '02',
    'марта': '03',
    'апреля': '04',
    'мая': '05',
    'июня': '06',
    'июля': '07',
    'августа': '08',
    'сентября': '09',
    'октрября': '10',
    'ноября': '11',
    'декабря': '12'
}

def quick_sort(seq: list):
    if len(seq) <= 1:
        return
    barrier = seq[0]['date_num']
    L, R, M = [], [], []
    for x in seq:
        if x['date_num'] < barrier:
            L.append(x)
        elif x['date_num'] == barrier:
            M.append(x)
        else:
            R.append(x)
    quick_sort(L)
    quick_sort(R)
    k = 0
    for x in L + M + R:
        seq[k] = x
        k += 1
