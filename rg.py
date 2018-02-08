import sys
import commands
import tools


def add(*add_args):
    if add_args[0] == 'band':
        b, l = commands.add.band(add_args[1])
        # Fucking Plaid Dracula...
        # Need to validate the location before importing it
        if l is not None and ('city' not in l.keys() or 'state' not in l.keys()):
            l = None
        if l is None:
            if 'hometown' in b:
                l = tools.pushpin.locate(b['hometown'])
            while l is None:
                l = tools.pushpin.locate(raw_input('Where is %s from? ' % b['name']))
        c = commands.add.city(l['city'])
        commands.connect.band_to_city(b['username'], c['name'])
        commands.connect.city_to_state(c['name'], l['state'])

    elif add_args[0] == 'bands':
        filepath = ''

        if len(add_args) == 4:
            filepath = add_args[3]
        elif len(add_args) == 3:
            filepath = add_args[2]

        with open(filepath, 'r') as lst:
            bandlist = lst.read().split('\n')

        for band in bandlist:
            add(*['band', band])

    elif add_args[0] == 'venue':
        try:
            # If argument is numeric, search by id:
            float(add_args[1])
            v, l = commands.add.venue(id=add_args[1])
        except:
            # Otherwise, search by username:
            v, l = commands.add.venue(add_args[1])
        while l is None:
            l = tools.pushpin.locate(raw_input('Where is %s located? ' % v['name']))
        c = commands.add.city(l['city'])
        commands.connect.venue_to_city(v, c)
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
