from py2neo import Graph, Node, Relationship, ConstraintError

import config
from Legacy import error

try:
    db = Graph(password=config.db_password)
except error.types as e:
    error.handle(e)


def check_node(label, key, value):
    node = db.find_one(label, key, value)
    return node is not None


def add_node(label, **properties):
    node = Node(label, **properties)
    try:
        rtn = db.create(node)
        return rtn
    except ConstraintError:
        db.merge(node, 'id', properties['id'])
        for prop in properties.keys():
            node[prop] = properties[prop]
        node.push()
    # return db.create(node)


def get_node(label, key, value):
    node = db.find_one(label, key, value)
    return node


def get_all_nodes(label):
    nodes = db.find(label)
    return nodes


def check_relationship(node1, relationship_type, node2=None):
    rel = db.match_one(start_node=node1, rel_type=relationship_type, end_node=node2)
    return rel is not None


def add_relationship(node1, relationship_type, node2):
    rel = Relationship(node1, relationship_type, node2)
    rtn = db.create(rel)
    return rtn


def get_relationship(node1, relationship_type, node2):
    rel = db.match_one(node1, relationship_type, node2)
    return rel,

