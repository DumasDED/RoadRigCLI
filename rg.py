import sys
import commands
import tools


def add(*add_args):
    if add_args[0] == 'band':
        b, l = commands.add.band(add_args[1])
        if l is None:
            if 'hometown' in b:
                l = tools.pushpin.locate(b['hometown'])
            while l is None:
                l = tools.pushpin.locate(raw_input('Where is %s from? ' % b['name']))
        c = commands.add.city(l['city'])
        commands.connect.band_to_city(b['username'], c['name'])
        commands.connect.city_to_state(c['name'], l['state'])

    elif add_args[0] == 'venue':
        v, l = commands.add.venue(add_args[1])
        while l is None:
            l = tools.pushpin.locate(raw_input('Where is %s located? ' % v['name']))
        c = commands.add.city(l['city'])
        commands.connect.venue_to_city(v['username'], c['name'])
        commands.connect.city_to_state(c['name'], l['state'])

    elif add_args[0] == 'events':
        band = None
        for i, arg in enumerate(add_args[1:]):
            if arg in ['with', 'featuring']:
                band = add_args[i+2]
        commands.scan.events_by_band(band)

args = sys.argv[1:]

if args[0] == 'add':
    add(*args[1:])
