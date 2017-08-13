import config
import error

from py2neo import Graph, Node, Relationship, GraphError

try:
    db = Graph(password=config.db_password)
except error.types as e:
    error.handle(e)


def check_node(label, key, value):
    node = db.find_one(label, key, value)
    return node is not None


def add_node(label, **properties):
    node = Node(label, **properties)
    return db.create(node)


def get_node(label, key, value):
    node = db.find_one(label, key, value)
    if node is None:
        raise GraphError("No %s found with %s '%s'." % (label, key, value))
    return node


def check_relationship(node1, relationship_type, node2):
    rel = db.match_one(node1, relationship_type, node2)
    return rel is not None


def add_relationship(node1, relationship_type, node2):
    rel = Relationship(node1, relationship_type, node2)
    db.create(rel)
