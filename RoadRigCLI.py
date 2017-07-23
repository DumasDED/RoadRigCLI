import sys
import config

from commands import *

args = sys.argv[1:]

if args[0].lower() in ['?', 'help']:
    print config.help

elif 'add' == args[0].lower():
    add(*args[1:])

elif 'connect' == args[0].lower():
    connect(*args[1:])

elif 'peruse' == args[0].lower():
    peruse(*args[1:])

elif 'config' == args[0].lower():
    print "Let's configure something."

else:
    print "'%s' is not a recognized rg command" % args[0]