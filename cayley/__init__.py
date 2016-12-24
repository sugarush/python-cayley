import json

from abc import ABCMeta, abstractmethod

from requests import Request, Session


class InvalidQuad(Exception):
    pass


class CayleyABC(object):

    __metaclass__ = ABCMeta

    def __init__(self, host='http://localhost:64210', version='v1'):
        self.host = host
        self.version = version
        self.graph = pyley.GraphObject()
        self.initialize()

    def url(self, path):
        return '%s/api/%s%s' % (self.host, self.version, path)

    def validate(self, quad):
        _object = quad.get('object')
        if not isinstance(_object, str):
            return False

        predicate = quad.get('predicate')
        if not isinstance(predicate, str):
            return False

        subject = quad.get('subject')
        if not isinstance(subject, str):
            return False

        label = quad.get('label')
        if not (label is None):
            if not isinstance(label, str):
                return False

        return True

    def validate_quads(self, quads):
        if not all(map(self.validate, quads)):
            raise InvalidQuad('Missing or invalid object, predicate or subject.')

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def run(self, query):
        pass

    @abstractmethod
    def write(self, quads):
        pass

    @abstractmethod
    def delete(self, quads):
        pass


class CayleyClient(CayleyABC):

    def initialize(self):
        self.client = Session()

    def fetch(self, path, **kargs):
        kargs['method'] = kargs.get('method', 'POST')
        kargs['url'] = self.url(path)
        request = Request(**kargs)
        return self.client.send(request)

    def run(self, query):
        response = self.fetch('/query/gremlin', data=str(query))
        return response.json()

    def write(self, quads):
        self.validate_quads(quads)
        response = self.fetch('/write', data=json.dumps(quads))
        return response.json()

    def delete(self, quads):
        self.validate_quads(quads)
        response = self._fetch('/delete', data=json.dumps(quads))
        return response.json()
