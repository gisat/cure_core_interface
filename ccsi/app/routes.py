from flask import Response, request, jsonify


from flask_restful import Resource, Api
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from ccsi.containers import app_containers
from ccsi.app.api_schema import api_schemas
from copy import deepcopy

# restful api
search_api = Api()
# apispec
docs = FlaskApiSpec()


class AtomEndpoint:

    def data_endpoint_url(self):
        """generate endpoint url. If it is 'base' service, service name is not included in url"""
        if self.service_name == 'base':
            return '/atom/search'.lower()
        return f'/{self.service_name}/atom/search'.lower()

    def get(self):
        process_request = request.args.to_dict()
        if self.catalogue:
            process_request.update({'cataloque': self.catalogue})
        if self.collection:
            process_request.update({'collection': self.collection})
        query = app_containers.request_processor.build_query(request, process_request)
        if query.valid:
            query.send_request()
        if query.valid:
            return Response(query.to_xml(), mimetype='application/xml', content_type='text/xml; charset=utf-8')


class JsonEndpoint:

    def data_endpoint_url(self):
        """generate endpoint url. If it is 'base' service, service name is not included in url"""
        if self.service_name == 'base':
            return '/json/search'.lower()
        return f'/{self.service_name}/json/search'.lower()

    def get(self):
        process_request = request.args.to_dict()
        if self.catalogue:
            process_request.update({'cataloque': self.catalogue})
        if self.collection:
            process_request.update({'collection': self.collection})
        query = app_containers.request_processor.build_query(request, process_request)
        if query.valid:
            query.send_request()
        if query.valid:
            return Response(query.to_json(), mimetype='application/json', content_type='application/json; charset=utf-8')


class AtomDescription:

    def data_endpoint_url(self):
        """generate endpoint url. If it is 'base' service, service name is not included in url"""
        if self.service_name == 'base':
            return '/atom/search/description.xml'.lower()
        return f'/{self.service_name}/atom/search/description.xml'.lower()

    def get(self):
        return Response(self.description.document(self.data_endpoint_url(), 'application/xml'),
                        mimetype='application/xml', content_type='text/xml; charset=utf-8')


class JsonDescription:

    def data_endpoint_url(self):
        """generate endpoint url. If it is 'base' service, service name is not included in url"""
        if self.service_name == 'base':
            return '/json/search/description.xml'.lower()
        return f'/{self.service_name}/json/search/description.xml'.lower()

    def get(self):
        return Response(self.description.document(self.data_endpoint_url(), 'application/json'),
                        mimetype='application/xml', content_type='text/xml; charset=utf-8')


class DescriptionFactory:

    @staticmethod
    def create(service_name, format, **ignore):
        description = app_containers.description_documents.get(service_name)
        cls_props = {'service_name': service_name,
                     'description': description}
        if format == 'json':
            cls_name = f'desjson{service_name}'.lower()
            return type(cls_name, (MethodResource, Resource, JsonDescription), cls_props)
        elif format == 'atom':
            cls_name = f'desatom{service_name}'.lower()
            return type(cls_name, (MethodResource, Resource, AtomDescription), cls_props)


class DataEndpointFactory:

    @staticmethod
    def create(service_name, format,  collection=None, catalogue=None, **ignore):
        cls_props = {'service_name': service_name,
                     'collection': collection,
                     'catalogue': catalogue}
        if format == 'json':
            cls_name = f'json{service_name}'.lower()
            return type(cls_name, (MethodResource, Resource, JsonEndpoint), cls_props)
        elif format == 'atom':
            cls_name = f'atom{service_name}'.lower()
            return type(cls_name, (MethodResource, Resource, AtomEndpoint), cls_props)


class SearchEndpoints:

    @staticmethod
    def register(properties, description):
        swagger_desc = description.get('swagger_desc')
        api_schema = description.get('api_schema')

        for format in ['json', 'atom']:
            Endpoint = DataEndpointFactory.create(**properties, format=format)
            doc_decorator = doc(description=swagger_desc, tags=[format])
            doc_use_kwargs = use_kwargs(api_schemas.get(api_schema), location=('json'))
            Endpoint = doc_decorator(Endpoint)
            Endpoint = doc_use_kwargs(Endpoint)
            endpoint = Endpoint()
            description = DescriptionFactory.create(**properties, format=format)()
            print('//// url ///')
            print(endpoint.data_endpoint_url())
            print(description.data_endpoint_url())

            search_api.add_resource(endpoint, endpoint.data_endpoint_url(), endpoint=endpoint.__class__.__name__)
            search_api.add_resource(description, description.data_endpoint_url(), endpoint=description.__class__.__name__)
            docs.register(endpoint.__class__, endpoint=endpoint.__class__.__name__.lower())


    @staticmethod
    def create(services):
        for service in services:
            SearchEndpoints.register(**service)


services = [{'properties': {'service_name': 'base',
                            'collection': None,
                            'catalogue': None},
             'description': {'swagger_desc': 'General endpoint to access all registred datasets',
                             'api_schema': 'base'}},
           {'properties': {'service_name': 'mundi_clms',
                                        'collection': 'clms',
                                        'catalogue': None},
                         'description': {'swagger_desc': 'General endpoint to access products from Mundi CLMS',
                                         'api_schema': 'mundi_clms'}}]



properties={'service_name': 'base',
            'collection': None,
            'catalogue': None}


SearchEndpoints.create(services)

