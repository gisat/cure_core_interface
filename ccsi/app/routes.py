from flask import Response, request
from flask_restful import Resource, Api
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import use_kwargs, doc
from flask_apispec.views import MethodResource
from ccsi.containers import app_containers
from ccsi.app.api_schema import api_schemas
from ccsi.config import config

# restful api
search_api = Api()
# apispec
docs = FlaskApiSpec()


class Endpoint:

    def process_request(self, request)-> dict:
        """
        Transform incoming request into data structure expected by Query class
        :return dict {  original_args: original query parameters,
                        process_args: working query parameters, mutable
                        base_url: incoming url
        """
        original_args, process_args, base_url, host_url = request.args.to_dict(), request.args.to_dict(), request.url, \
                                                          request.host_url
        if self.resource:
            process_args.update({'resource': self.resource})
        if self.collection:
            process_args.update({'collection': self.collection})
        return {'original_args': original_args,
                'process_args': process_args,
                'base_url': base_url,
                'host_url': host_url}


class AtomEndpoint(Endpoint):

    def data_endpoint_url(self):
        """generate endpoint url. If it is 'base' service, service name is not included in url"""
        if self.service_name == 'base':
            return '/atom/search'.lower()
        return f'/{self.service_name}/atom/search'.lower()

    def get(self):
        process_request = self.process_request(request)
        query = app_containers.request_processor.build_query(**process_request)
        if query.valid:
            query.send_request()
        if query.valid:
            if self.service_name == 'base':
                return Response(query.base_to_xml(), mimetype='application/xml', content_type='text/xml; charset=utf-8')
            return Response(query.to_xml(), mimetype='application/xml', content_type='text/xml; charset=utf-8')



class JsonEndpoint(Endpoint):

    def data_endpoint_url(self):
        """generate endpoint url. If it is 'base' service, service name is not included in url"""
        if self.service_name == 'base':
            return '/json/search'.lower()
        return f'/{self.service_name}/json/search'.lower()

    def get(self):
        process_request = self.process_request(request)
        query = app_containers.request_processor.build_query(**process_request)
        if query.valid:
            query.send_request()
        if query.valid:
            if self.service_name == 'base':
                return Response(query.base_to_json(), mimetype='application/json', content_type='application/json; charset=utf-8')
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
    def create(service_name, format,  collection=None, resource=None, **ignore):
        cls_props = {'service_name': service_name,
                     'collection': collection,
                     'resource': resource}
        if format == 'json':
            cls_name = f'json{service_name}'.lower()
            return type(cls_name, (MethodResource, Resource, JsonEndpoint), cls_props)
        elif format == 'atom':
            cls_name = f'atom{service_name}'.lower()
            return type(cls_name, (MethodResource, Resource, AtomEndpoint), cls_props)


class SearchEndpointsFactory:

    @staticmethod
    def register(endpoint, endpoint_description):
        search_api.add_resource(endpoint, endpoint.data_endpoint_url(), endpoint=endpoint.__class__.__name__)
        docs.register(endpoint.__class__, endpoint=endpoint.__class__.__name__.lower())
        search_api.add_resource(endpoint_description, endpoint_description.data_endpoint_url(),
                                endpoint=endpoint_description.__class__.__name__)

    @staticmethod
    def swagger_spec(cls, swagger_desc, api_schema, tag):
        doc_decorator = doc(description=swagger_desc, tags=tag)
        doc_use_kwargs = use_kwargs(api_schemas.get(api_schema), location=('json'))
        cls = doc_decorator(cls)
        cls = doc_use_kwargs(cls)
        return cls

    @staticmethod
    def create_endpoint(format, properties, description, **ignore):
        Endpoint = DataEndpointFactory.create(**properties, format=format)
        endpoint = SearchEndpointsFactory.swagger_spec(Endpoint, **description)()
        return endpoint

    @staticmethod
    def create_description(format, properties, **ignore):
        endpoint_description = DescriptionFactory.create(**properties, format=format)()
        return endpoint_description

    @staticmethod
    def create(services):
        for service in services:
            for format in ['json', 'atom']:
                endpoint = SearchEndpointsFactory.create_endpoint(format, **service)
                endpoint_description = SearchEndpointsFactory.create_description(format, **service)
                SearchEndpointsFactory.register(endpoint, endpoint_description)

SearchEndpointsFactory.create(config.ENDPOINTS)

