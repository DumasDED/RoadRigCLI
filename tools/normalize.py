import unicodedata


def normalize_obj(item):
    for k in item.keys():
        if type(item[k]) is unicode:
            item[k] = unicodedata.normalize('NFKD', item[k]).encode('ascii', 'ignore')
        elif type(item[k]) is dict:
            normalize_obj(item[k])
    return item
