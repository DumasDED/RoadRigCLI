import sys

from commands import *

args = [arg.lower() for arg in sys.argv[1:]]


if args[0] in ['?', 'help']:
    print config.help


elif 'add' == args[0].lower():

    if len(args) == 0:
        print 'Please specify entity to add.'

    elif args[1] == 'band':
        Legacy.add.band(*args[2:])

    elif args[1] == 'bands':
        if args[2] == 'from' and args[3] == 'file' and '.' in args[4]:
            lst = parse.text_file(args[4])
            for row in lst:
                Legacy.add.band(*row)
        elif args[2] == 'from' and '.' in args[3]:
            lst = parse.text_file(args[3])
            for row in lst:
                Legacy.add.band(*row)
        else:
            print "'%s' is not a recognized command. Please specify a filename." % string.join(args[2:])

    elif args[1] == 'venue':
        Legacy.add.venue(*args[2:])

    else:
        print "'%s' is not a recognized entity to add." % args[1]


elif 'connect' == args[0].lower():
    connect(*args[1:])

elif 'peruse' == args[0].lower():
    peruse(*args[1:])

elif 'config' == args[0].lower():
    print "Let's configure something."

else:
    print "'%s' is not a recognized rg command" % args[0]