import string
import parse

from add import *
from connect import *
from peruse import *


# Eventually all of these will be wrapped into the RoadRigCLI file and this file will replace cmds.py as a
# barrel (?) for all of the command files (i.e. add, connect, peruse)


def add(*args):
    pass

    # if len(args) == 0:
    #     print 'Please specify entity to add.'
    #
    # elif args[0] == 'band':
    #     band(*args[1:])
    #
    # elif args[0] == 'bands':
    #     if args[1] == 'from' and args[2] == 'file' and '.' in args[3]:
    #         lst = parse.text_file(args[3])
    #         for name in lst:
    #             band(name)
    #     elif args[1] == 'from' and '.' in args[2]:
    #         lst = parse.text_file(args[2])
    #         for name in lst:
    #             band(name)
    #     else:
    #         print "'%s' is not a recognized command. Please specify a filename." % string.join(args[1:])
    #
    # elif args[0] == 'venue':
    #     venue(*args[1:])
    #
    # else:
    #     print "'%s' is not a recognized entity to add." % args[0]


def connect(*args):
    if len(args) == 0:
        print 'Please specify entities to connect.'

    elif args[1].lower() not in ['with', 'to', 'and'] or len(args) != 3:
        print "'%s' is not a recognized command string." % (string.join(args, ' '))

    else:
        band_to_band(args[0], args[2])


def peruse(*args):
    if len(args) == 0:
        print 'Please specify entity to peruse.'

    else:
        events(args[0])
