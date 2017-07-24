import error

def location(r):
    r = r.copy()
    try:
        if 'location' in r:
            l = r['location']
            r.pop('location', None)
            c = l['city']
            s = l['state']
            return r, c, s
        else:
            return r, None, None
    except KeyError as e:
        raise KeyError("Location could not be parsed. No value available for %s." % e)


def text_file(name):
    f = open(name, 'r')
    l = f.read().split('\n')
    f.close()
    return l
