import requests
import py2neo

types = (requests.exceptions.HTTPError, py2neo.ConstraintError, py2neo.GraphError, KeyError)


def handle(exception, *args):
    if isinstance(exception, requests.exceptions.HTTPError):
        if exception.response.status_code == 404:
            print "%s not found." % args[0]
        elif exception.response.status_code == 400:
            print "There was a problem retrieving %s from Facebook:" % args[0]
            print exception.message.split('Please read the Graph API documentation')[0]     # Patronizing fucks...
        else:
            raise
    elif isinstance(exception, py2neo.ConstraintError):
        print "%s already exists in the database." % args[0]
    elif isinstance(exception, py2neo.GraphError):
        print "There was a problem accessing the database:"
        print exception
    elif isinstance(exception, KeyError):
        print "There was a problem parsing a data object:"
        print exception
