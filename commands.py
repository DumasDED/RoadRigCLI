import string

from add import *
from connect import *
from peruse import *


def add(*args):

    if len(args) == 0:
        print 'Please specify entity to add.'

    elif args[0] == 'band':
        band(*args[1:])

    elif args[0] == 'venue':
        venue(*args[1:])

    else:
        print "'%s' is not a recognized entity to add." % args[0]


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
