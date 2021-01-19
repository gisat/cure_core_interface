from marshmallow import Schema, fields
from ccsi.containers import app_containers
'''
This module serve to create marshmallow schema for swager from service parameters
'''

MAP = {'StringParameter': fields.String(),
       'IntParameter': fields.Integer(),
       'BBoxParameter': fields.String(),
       'WKTParameter': fields.String(),
       'FloatParameter': fields.Float(),
       'DateTimeParameter': fields.DateTime(),
       'OptionParameter': fields.String()}


def schema_from_service(service_name=None):
    return Schema.from_dict({name: MAP.get(parameter) for name, parameter
                             in get_endpoint_params(service_name).items()})


def get_endpoint_params(service_name=None) -> dict:
    endpoint_params = {}
    fileds = set()
    if service_name:
        for name, parameter in app_containers.services.get(service_name).input_parameters().items():
            endpoint_params.update({name: parameter.__class__.__name__})
    else:
        for name, services in app_containers.parameter_register.items():
            for service in services:
                fileds.add(service.input_parameter(name).__class__.__name__)
            if len(fileds) > 1:
                raise ValueError(f'Api Schema creation error. Different parameter types for parameter {name}')
            endpoint_params.update({name: fileds.pop()})
            fileds = set()
    return endpoint_params


api_schemas = {service.service_name: schema_from_service(service.service_name) for service in
               app_containers.services_register.__iter__()}
api_schemas.update({'base': schema_from_service()})
