from flask import Response
from flask import request as request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource, Api
from flask_apispec.extension import FlaskApiSpec
from ccsi.containers import app_containers
from ccsi.app.api_schema import api_schemas

# restful api
search_api = Api()
# apispec
docs = FlaskApiSpec()


@doc(description='Global endpoint to all registred resources', tags=['Json'])
@use_kwargs(api_schemas.get('base'), location=('json'))
class JsonFormat(MethodResource, Resource):
    def get(self):
        query = app_containers.request_processor.build_query(request)
        if query.valid:
            query.send_request()
        if query.valid:
            response = Response(query.to_json(), mimetype='application/json',
                                content_type='application/json; charset=utf-8')
            return response

@doc(description='Global endpoint to all registred resources', tags=['Atom'])
@use_kwargs(api_schemas.get('base'), location=('json'))
class AtomFormat(MethodResource, Resource):
    def get(self):
        query = app_containers.request_processor.build_query(request)
        if query.valid:
            query.send_request()
        if query.valid:
            response = Response(query.to_xml(), mimetype='application/xml', content_type='text/xml; charset=utf-8')
            return response

class DescriptionAtomFormat(MethodResource, Resource):
    ENDPOINT = '/atom/search/description'
    def get(self):
        mimetype = 'application/xml'
        description = app_containers.description_documents.get('base')
        response = Response(description.document(DescriptionAtomFormat.ENDPOINT, mimetype),
                            mimetype=mimetype, content_type='text/xml; charset=utf-8')
        return response

search_api.add_resource(JsonFormat, '/json/search', endpoint=JsonFormat.__name__.lower())
search_api.add_resource(AtomFormat, '/atom/search', endpoint=AtomFormat.__name__.lower())
search_api.add_resource(DescriptionAtomFormat, DescriptionAtomFormat.ENDPOINT, endpoint=DescriptionAtomFormat.__name__.lower())

docs.register(AtomFormat, endpoint=AtomFormat.__name__.lower())
docs.register(JsonFormat, endpoint=JsonFormat.__name__.lower())


