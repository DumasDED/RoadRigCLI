import PushPin


def location(r):
    r, c, s = r.copy(), None, None
    if 'location' in r:
        l = r['location']
        r.pop('location', None)
        c = l['city'] if 'city' in l else None
        s = l['state'] if 'state' in l else None
    elif 'hometown' in r:
        c, s = PushPin.locate(r['hometown'])
    return r, c, s


def text_file(name):
    f = open(name, 'r')
    l = f.read().split('\n')
    f.close()
    return [i.split(', ') for i in l]
