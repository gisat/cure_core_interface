from ccsi.config import Config
from ccsi.search.service.services import Services
from ccsi.errors.errors import Error
from ccsi.schema.opensearch import open_search_response
from lxml import etree
from flask import request as frequest



class Query:

    def __init__(self, org_request, services):
        self.org_request = org_request
        self.request_args = self._lower(self.org_request)
        self.services = services
        self.error = {}
        self.responses = {}
        self.entries = []

    @classmethod
    def create(cls, services):
        """create from flask request variable"""
        org_request = frequest.args.copy()
        return cls(org_request, services)

    @property
    def valid(self):
        if len(self.error) == 0:
            return True
        return False

    @property
    def totalresults(self):
        return str(len(self.entries))

    def send_request(self):
        if self.valid:
            for service in self.services:
                output = service.send_request(self.request_args)
                if isinstance(output, dict):
                    self.error.update(output)
                else:
                    self.entries += output


    @staticmethod
    def _lower(dictionary: dict):
        """turn dictionry keys and values to lower case"""
        return {key.lower(): value.lower() for key, value in dictionary.items()}

    def to_xml(self):
        feed = open_search_response.atom_head(self.request_args, self.totalresults, 'foo.bar', str(1),
                                              self.request_args.get('maxrecords'))
        for entry in self.entries:
            feed.append(entry.to_xml())
        return etree.tostring(feed, pretty_print=True).decode("utf-8")

    def to_json(self):
        pass

class Register:

    def __init__(self):
        self._services = Services.create()
        self._default_params = self._crt_default_register()
        self._parameter_register = self._crt_parameters_register()
        self._services_register = {self.service(service) for service in self.services()}

    @classmethod
    def create(cls):
        return cls()

    @property
    def default_parameters(self):
        return self._default_params

    @property
    def parameters_register(self):
        return self._parameter_register

    @property
    def services_register(self):
        return self._services_register

    def services(self):
        return self._services.services()

    def service(self, service_name):
            return self._services.service(service_name)

    def _crt_parameters_register(self):
        register = {}
        for service_name in self.services():
            service = self.service(service_name)
            for parameter in service.input_parameters().keys():
                if register.__contains__(parameter):
                    register[parameter].add(service)
                else:
                    register.update({parameter: {service}})
        return register

    def _crt_default_register(self):
        return {parameter.get('name'): parameter.get('default') for parameter in
         Config.SERVICE_PARAMETERS.get('base') if parameter.get('default') is not None}


class RequestProcessor:
    PROCESSES = ['_check_default', '_check_request_key', '_process_request']

    def __init__(self, services, register):
        self._services = services
        self._register = register

    @classmethod
    def create(cls):
        services = Services.create()
        register = Register.create()
        return cls(services, register)

    @property
    def register(self):
        return self._register

    @property
    def services(self):
        return self._services.services()

    def service(self, service_name):
        return self._services.service(service_name)

    def build_query(self):
        query = Query.create(self.register.services_register)
        for process in self.PROCESSES:
            getattr(self, process)(query)
            if query.valid is False:
                break
        return query

    def _check_default(self, query: Query):
        for key, value in self.register.default_parameters.items():
            if not query.org_request.__contains__(key):
                if isinstance(value, list):
                    query.request_args.update({key: value})
                else:
                    query.request_args.update({key: value})
        return query

    def _process_request(self, query: Query):
        for parameter, value in query.request_args.items():
            self._find_relevant_services(query, parameter, value)
        return query

    def _find_relevant_services(self, query: Query, parameter, value):
        query.services = self.register.parameters_register.get(parameter).intersection(query.services)
        # validation of service input parameter
        services = query.services.copy()
        for service in services:
            if parameter in service.mapped.keys():
                validator = service.parameter(parameter).validate(value)
                if validator is not True:
                    query.error.update({'invalid value': validator})
            elif service.service_name == 'base':
                query.services.remove(service)
            else:
                value = self._check_tag_value_type(value)
                if not all(val in value for val in getattr(service, parameter)):
                    query.services.remove(service)

        return query

    def _check_request_key(self, query: Query):
        for key in query.request_args.keys():
            if not key in self.register.parameters_register.keys():
                query.error.update({'invalid parameter': Error.invalid_parameter([key])})
        return query

    @staticmethod
    def _check_tag_value_type(value):
        """expected tag value is list, single string or list represent as comma delimited string"""
        if isinstance(value, list):
            return value
        elif value.find(',') != -1:
            return value.split(',')
        elif isinstance(value, str):
            return [value]
        else:
            raise TypeError(f'Unexpected type of service tag value. Type of value: {value} is {type(value)}')


request_processor = RequestProcessor.create()


