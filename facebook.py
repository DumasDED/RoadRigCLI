import config
import requests

p = {'access_token': '%s|%s' % (config.app_id, config.app_secret)}


def get(handle, **kwargs):
    for key, value in kwargs.iteritems():
        p[key] = value
    r = requests.get('%s/%s' % (config.app_url, handle), p)
    if r.status_code != 200:
        raise requests.exceptions.HTTPError(r.json()['error']['message'], response=r)
    return r.json()
