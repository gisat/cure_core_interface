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


def schema_from_service(service_name):
    return Schema.from_dict({name: MAP.get(parameter) for name, parameter
                             in get_endpoint_params(service_name).items()})

def get_endpoint_params(service_name: str) -> dict:
    endpoint_params = {}
    for name, parameter in app_containers.services.get(service_name).input_parameters().items():
        endpoint_params.update({name: parameter.__class__.__name__})
    return endpoint_params

def schema_from_base():
    endpoint_params = {name: app_containers.service_parameters.get('base').parameter(name).__class__.__name__
                       for name in app_containers.service_parameters.get('base').parameters()}

    for service_name in app_containers.services.keys():
        service_params = get_endpoint_params(service_name)
        endpoint_params = {**endpoint_params, **service_params}
    return Schema.from_dict({name: MAP.get(parameter) for name, parameter in endpoint_params.items()})




api_schemas = {service.service_name: schema_from_service(service.service_name) for service in
               app_containers.services_register.__iter__()}
api_schemas.update({'base': schema_from_base()})
