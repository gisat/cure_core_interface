from ccsi.config import config
from ccsi.app.search.service.connection import Connection
from ccsi.app.search.service.parameters import ServiceParameters
from ccsi.app.search.service.services import Service
from ccsi.app.search.response.parsers import response_parser_builder
from ccsi.app.search.response.entry import Entry
from ccsi.app.search.main import Register, RequestProcessor
from ccsi.app.open_description import DescriptionDocument


class Containers:

    def __init__(self, config):
        self.connections = {service_name: Connection.create(**config.CONNECTION_.get(service_name)) for service_name in
                            config.SERVICES_}
        self.entry_register = self.create_entry_register()
        self.response_parsers = {service_name: response_parser_builder.build(self.entry_register.get(service_name),
                                 **config.RESPONSE_PARSERS_.get(service_name)) for service_name in config.SERVICES_}
        self.service_parameters = {service_name:  ServiceParameters.create(config.SERVICE_PARAMETERS.get(service_name))
                                   for service_name in config.SERVICE_PARAMETERS.keys()}
        self.mapped_pairs = config.MAPED_PAIRS
        self.services = {service_name: self.service_factory(service_name) for
                         service_name in config.SERVICES_}
        self.parameter_register = self.create_parameter_register()
        self.service_tag_register = self.create_service_tag_register(config.SERVICE_TAGS)
        self.default_parameters_register = self.create_default_parameters_register()
        self.services_register = {self.get_service(service_name)for service_name in config.SERVICES_}
        self.register = Register.create(self.services_register, self.parameter_register, self.service_tag_register,
                                        self.default_parameters_register)
        self.request_processor = RequestProcessor.create(self.register)
        self.description_documents = self.create_description_documents()

    def get_connection(self, service_name) -> Connection:
        return self.connections.get(service_name)

    def get_response_parser(self, service_name):
        return self.response_parsers.get(service_name)

    def get_service_parameters(self, service_name) -> ServiceParameters:
        return self.service_parameters.get(service_name)

    def get_mapped_pair(self, service_name) -> dict:
        return self.mapped_pairs.get(service_name)

    def get_service(self, service_name) -> Service:
        return self.services.get(service_name)

    def get_parameter_register(self, parameter_name) -> list:
        return self.parameter_register.get(parameter_name)

    def get_service_tag_register(self, parameter_name) -> dict:
        return self.service_tag_register.grt(parameter_name)

    def get_default_parameters_register(self, parameter_name):
        return self.default_parameters_register.get(parameter_name)

    def service_factory(self, service_name: str) -> Service:
        """factory method create service"""
        parameters = self.get_service_parameters(service_name)
        mapped = self.get_mapped_pair(service_name)
        connection = self.get_connection(service_name)
        response_parser = self.get_response_parser(service_name)
        return Service.create(service_name, parameters, mapped, connection, response_parser)

    def create_parameter_register(self):
        """create register of all api input parameters ie. from base api and custom for given connected service"""
        register = {}
        for service_name, items in self.mapped_pairs.items():
            for key in items.keys():
                if register.__contains__(key):
                    register[key].add(self.get_service(service_name))
                else:
                    register.update({key: {self.get_service(service_name)}})
        return register

    def create_service_tag_register(self, service_tags):
        """register of service tags"""
        register = service_tags
        for parameter, tags in register.items():
            for tag, service_names in tags.items():
                register[parameter][tag] = [self.get_service(service_name) for service_name in service_names]
        return register

    def create_default_parameters_register(self):
        return {parameter.name: parameter.default for parameter in self.get_service_parameters('base') if
                parameter.default is not None}

    @staticmethod
    def create_entry_register():
        register = {}
        for service_name, entry_parameters in config.ENTRY_MAPED_PAIRS.items():
            properties = {parameter_name: config.ENTRY_PARS.get(parameter_name)
                          for parameter_name in entry_parameters.keys()}
            register.update({service_name: Entry.create(properties)})
        return register

    def create_description_documents(self):
        documents = {service_name: DescriptionDocument.create(config.PARAMETERS_DESCRIPTION, service) for service_name,
                     service in self.services.items()}
        documents.update({'base': DescriptionDocument.create(config.PARAMETERS_DESCRIPTION)})
        return documents


app_containers = Containers(config)
