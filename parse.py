def location(r):
    r = r.copy()
    if 'location' in r:
        l = r['location']
        r.pop('location', None)
        c = l['city'] if 'city' in l else None
        s = l['state'] if 'state' in l else None
        return r, c, s
    else:
        return r, None, None


def text_file(name):
    f = open(name, 'r')
    l = f.read().split('\n')
    f.close()
    return [i.split(', ') for i in l]
