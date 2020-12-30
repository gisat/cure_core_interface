from ccsi.errors.errors import Error
from ccsi.schema.opensearch import OpenSearchResponse
from lxml import etree
from copy import deepcopy
from geojson import FeatureCollection


class Query:

    def __init__(self, request, services):
        self._request = request
        self.process_request = self._lower(self._request.args)
        self.services = services
        self.error = {}
        self.responses = {}
        self.entries = []

    @classmethod
    def create(cls, request, services):
        """create from flask request variable"""
        return cls(request, services)

    @property
    def valid(self):
        if len(self.error) == 0:
            return True
        return False

    @property
    def totalresults(self):
        return len(self.entries)

    def send_request(self):
        if self.valid:
            for service in self.services:
                output = service.send_request(self.process_request)
                if isinstance(output, dict):
                    self.error.update(output)
                else:
                    self.entries += output

    @staticmethod
    def _lower(dictionary: dict):
        """turn dictionry keys and values to lower case"""
        return {key.lower(): value.lower() for key, value in dictionary.items()}

    def to_xml(self):
        response = OpenSearchResponse(self._request, self.process_request, self.totalresults)
        feed = response.atom_head()
        for entry in self.entries:
            feed.append(entry.to_xml())
        return etree.tostring(feed, pretty_print=True).decode("utf-8")

    def to_json(self):
        response = OpenSearchResponse(self._request, self.process_request, self.totalresults)
        head = response.json_head()
        return FeatureCollection(features=[entry. to_json() for entry in self.entries], properties=head)


class Register:

    def __init__(self, services_register, parameter_register, service_tag_register, default_parameters_register):
        self.services_register = services_register
        self.parameter_register = parameter_register
        self.service_tag_register = service_tag_register
        self.default_parameters_register = default_parameters_register

    @classmethod
    def create(cls, services_register, parameter_register, service_tag_register, default_parameters_register):
        return cls(services_register, parameter_register, service_tag_register, default_parameters_register)

    def from_parameter_register(self, parameter_name):
        return self.parameter_register.get(parameter_name)

    def from_service_tag_register(self, tag):
        return self.service_tag_register.get(tag)

    def from_default_parameters_register(self, parameter_name):
        return self.default_parameters_register.get(parameter_name)

    def get_service_registr(self):
        return deepcopy(self.services_register)


class RequestProcessor:
    PROCESSES = ['check_request_key', 'check_default', 'find_service_by_tags', 'find_services_by_parameter']

    def __init__(self, register):
        self._register = register

    @classmethod
    def create(cls, register):
        return cls(register)

    @property
    def register(self):
        return self._register

    def build_query(self, request):
        query = Query.create(request, self.register.get_service_registr())
        for process in self.PROCESSES:
            getattr(self, process)(query)
            if query.valid is False:
                break
        return query

    def find_service_by_tags(self, query: Query) -> Query:
        """provide selection of services by tags"""
        for parameter_name in self.register.service_tag_register.keys():
            services = query.services
            tags = query.process_request.get(parameter_name)
            if tags.find(',') != -1:
                tag_services = {service for tag in tags.split(',') for service in
                                self.register.service_tag_register[parameter_name][tag]}
            else:
                tag_services = {service for service in self.register.service_tag_register[parameter_name][tags]}
            query.services = services.intersection(tag_services)
        return query

    def find_services_by_parameter(self, query: Query):
        """provide selection of services by request parameter ans validate them"""
        for parameter_name, value in query.process_request.items():
            services = query.services.copy()
            for service in services:
                if parameter_name not in self.register.default_parameters_register.keys():
                    validator = service.input_parameter(parameter_name)
                    if validator is None:
                        query.services.remove(service)
                    elif not validator.validate(value):
                        query.error.update({'invalid value': validator.validate(value)})
        return query

    def check_default(self, query: Query):
        """check if requset has default parameters and set their value """
        for parameter_name, value in self.register.default_parameters_register.items():
            if query.process_request.get(parameter_name) is None:
                query.process_request.update({parameter_name: ','.join(value)})
        return query

    def check_request_key(self, query: Query):
        """check if request has all valid keys """
        for parameter_name in query.process_request.keys():
            if ((self.register.parameter_register.get(parameter_name) is None) and
                    (parameter_name not in self.register.service_tag_register.keys())):
                query.error.update({'invalid parameter': Error.invalid_parameter([parameter_name])})
        return query




