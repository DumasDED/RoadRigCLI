import database as db


def relationship(node1, rel, node2=None):
    return db.get_relationship(node1, rel, node2)
