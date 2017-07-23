import config

from py2neo import Graph, Node, Relationship, GraphError

db = Graph(password=config.db_password)


def check_node(label, key, value):
    node = db.find_one(label, key, value)
    return node is not None


def add_node(label, **properties):
    node = Node(label, **properties)
    db.create(node)


def get_node(label, value, key='username'):
    node = db.find_one(label, key, value)
    if node is None:
        raise GraphError("No %s found with %s '%s'." % (label, key, value))
    return node


def add_relationship(node1, relationship_type, node2):
    rel = Relationship(node1, relationship_type, node2)
    db.create(rel)
