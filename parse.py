def location(r):
    r, c, s = r.copy(), None, None
    if 'location' in r:
        l = r['location']
        r.pop('location', None)
        c = l['city'] if 'city' in l else c
        s = l['state'] if 'state' in l else s
    if 'hometown' in r:
        h = r['hometown'].split(',') + [None, None]
        c = h[0] if c is None else c
        s = h[1] if s is None else s
    return r, c, s


def text_file(name):
    f = open(name, 'r')
    l = f.read().split('\n')
    f.close()
    return [i.split(', ') for i in l]
