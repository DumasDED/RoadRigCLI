def location(r):
    r = r.copy()
    if 'location' in r:
        l = r['location']
        r.pop('location', None)
        c = l['city']
        s = l['state']
        return r, c, s
    else:
        return r, None, None
