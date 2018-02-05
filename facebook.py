import config
import requests

from tools import normalize_obj

p = {'access_token': '%s|%s' % (config.app_id, config.app_secret)}


def get(handle, **kwargs):
    for key, value in kwargs.iteritems():
        p[key] = value

    r = requests.get('%s/%s' % (config.app_url, handle), params=p)

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.json()['error']['message'], response=r)

    rtn = r.json()

    # Normalize all unicode values:
    normalize_obj(rtn)

    return rtn


def get_attr(handle, attr_type, **kwargs):
    for key, value in kwargs.iteritems():
        p[key] = value

    r = requests.get('%s/%s/%s' % (config.app_url, handle, attr_type), params=p)
    rtn = []

    while True:
        if r.status_code != 200:
            raise requests.exceptions.HTTPError(r.json()['error']['message'], response=r)

        rtn.extend(r.json()['data'])

        if 'next' in r.json()['paging']:
            r = requests.get(r.json()['paging']['next'])
        else:
            # Normalize all unicode values:
            for r in rtn:
                normalize_obj(r)

            return rtn


def parse(node):
    l = None
    if 'location' in node:
        l = node.pop('location', None)
