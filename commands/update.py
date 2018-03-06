import database as db
import time

from tools import pushpin


def cities():
    cities = db.get_all_nodes('city')
    cities = list(cities)
    cities = [city for city in cities if not pushpin.intersect(city.keys(), ['north', 'south', 'east', 'west'])]

    for city in cities:
        state = db.get_relationship(city, 'is_in', None)[0].end_node()
        print "Adding viewport for city %s, %s..." % (city['name'], state['abbr'])
        bounds = pushpin.get_bounds('%s, %s' % (city['name'], state['abbr']))
        for key in bounds.keys():
            city[key] = bounds[key]
        db.add_node('city', 'name', **city)
        print "%s successfully updated." % city['name']
        time.sleep(1)

    print "Done."
