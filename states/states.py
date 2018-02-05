from py2neo import Graph, Node, ConstraintError

print "Parsing file 'states.txt'..."

file = open('states.txt', 'r')

list = file.read()

list = list.replace('"', '')

list = list.split('\n')

for i, item in enumerate(list):
    list[i] = item.split(',')

# list[-1][1] = 'WY'

print "Parsed. Accessing database..."

g = Graph(password='abc123=0')

for item in list:
    print "Adding %s..." % item[0]
    n = Node('state', name=item[0], abbr=item[1])
    try:
        g.create(n)
    except ConstraintError as e:
        print e.message

print "Done."
