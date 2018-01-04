import sys
import commands
import tools


def add(*add_args):
    print add_args[0]
    if add_args[0] == 'band':
        b, l = commands.add.band(add_args[1])
        if l is None:
            l = tools.pushpin.locate(b['hometown'])
            # l = dict(city=x['name'], state=y['abbr'])
            print l
        c = commands.add.city(l['city'])
        commands.connect.band_to_city(b, c)
        commands.connect.city_to_state(c, l['state'])


args = sys.argv[1:]

if args[0] == 'add':
    add(*args[1:])
