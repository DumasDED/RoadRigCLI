import config

from py2neo import Graph, Node, Relationship, GraphError

db = Graph(password=config.db_password)


def add_node(node_type, **properties):
    node = Node(node_type, **properties)
    db.create(node)


def get_node(node_type, handle):
    node = db.find_one(node_type, 'username', handle)
    if node is None:
        raise GraphError("No %s found with handle '%s'." % (node_type, handle))
    return node


def add_relationship(node1, relationship_type, node2):
    rel = Relationship(node1, relationship_type, node2)
    db.create(rel)
