from ccsi.config import Config
from ccsi.search.service.parameters import ServiceParameters
from ccsi.search.service.connection import Connection
from ccsi.search.entry.entry import response_parser_builder


class Service:

    def __init__(self, parameters, mapped, connection, catalogue, collection, service_name, response_parser):
        self._parameters = parameters
        self.mapped = mapped
        self.connection = connection
        self.catalogue = catalogue
        self.collection = collection
        self.service_name = service_name
        self.response_parser = response_parser

    @classmethod
    def create(cls, service_name):
        parameters = ServiceParameters.create(Config.SERVICE_PARAMETERS.get(service_name))
        mapped = Config.MAPED_PAIRS.get(service_name)
        connection = Connection.create(**Config.SERVICES.get(service_name))
        catalogue = Config.SERVICES.get(service_name).get('catalogue')
        collection = Config.SERVICES.get(service_name).get('collection')
        response_parser = response_parser_builder.build(**Config.SERVICES.get(service_name).get('response'))
        return cls(parameters, mapped, connection, catalogue, collection, service_name, response_parser)

    def send_request(self, request: dict):
        service_request = self.translate(request)
        query = self.transform(service_request)
        validation = self.validate(query)
        if validation is True:
            response = self.connection.send_request(query)
            if response.status_code != 200:
                return {'Connection fail': f'{self.service_name}:{response.status_code}'}
            return self.response_parser.parse(response)
        else:
            return validation

    def translate(self, request: dict):
        """find common parameters between service and base api and return dict with corresponding api parameters name
        """
        common_params = {name for name in self.mapped.keys()}.intersection({name for name in request.keys()})
        return {self.mapped.get(param): request.get(param) for param in common_params .__iter__()}

    def transform(self, service_request: dict):
        """transform value of base api into value expected by service"""
        return {name: self.parameter(name).transform(value) for name, value in service_request.items()}

    def validate(self, service_request: dict):
        """Validation of query parameters against types expected by service api parameters """
        report = {name: self.parameter(name).validate(value) for name, value in service_request.items()
                  if self.parameter(name).validate(value) is not True}
        if len(report) > 0:
            return report
        else:
            return True

    def parameter(self, name):
        """coll service parametr by orginal or mapped name"""
        try:
            return self._parameters.parameter(name)
        except AttributeError:
            return self._parameters.parameter(self.mapped.get(name))

    def parameters(self):
        """return original parameters of service"""
        return self._parameters.parameters()

    def input_parameters(self):
        """return expected input parameter i.e mapped plus catalogue and collection and default values, None mean any
        valid parameter"""
        input = {name: self.parameter(name).default for name in self.parameters()}
        if self.mapped is not None:
            for input_name, original_name in self.mapped.items():
                input[input_name] = input.pop(original_name)
        input.update({'collection': self.collection, 'catalogue': self.catalogue})
        return input


class Services:
    """class encapsulated all services"""

    def __init__(self, services):
        self._services = services

    @classmethod
    def create(cls):
        services = []
        for service_name in Config.SERVICES.keys():
            setattr(cls, service_name, Service.create(service_name))
            services.append(service_name)
        return cls(services)

    def services(self):
        return self._services

    def service(self, service_name: str):
        return getattr(self, service_name)