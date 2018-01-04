import googlemaps
import config


def intersect(list1, list2):
    return len(set(list1).intersection(set(list2))) != 0


def locate(query):

    gmaps = googlemaps.Client(key=config.g_key)

    result = gmaps.places(query=query)
    if result['status'] != 'OK':
        return None
    geo = result['results'][0]['geometry']['location']
    result = gmaps.reverse_geocode(latlng=geo)

    components = result[0]['address_components']

    country = [component for component in components if intersect(component['types'], ['country'])][0]

    if country['short_name'] != 'US':
        return None

    state = [component for component in components if intersect(component['types'], ['administrative_area_level_1'])][0]

    city = (
        [component for component in components if intersect(component['types'], ['locality'])]
         or
        [component for component in components if intersect(component['types'], ['sublocality', 'sublocality_level_1'])]
    )[0]

    result = {}
    result['city'] = city['short_name']
    result['state'] = state['short_name']
    return result
