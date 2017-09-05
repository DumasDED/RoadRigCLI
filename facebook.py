import config
import requests

p = {'access_token': '%s|%s' % (config.app_id, config.app_secret)}


def get(handle, **kwargs):
    for key, value in kwargs.iteritems():
        p[key] = value

    r = requests.get('%s/%s' % (config.app_url, handle), params=p)

    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.json()['error']['message'], response=r)

    return r.json()


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
            return rtn


def parse(node):
    l = None
    if 'location' in node:
        l = node.pop('location', None)