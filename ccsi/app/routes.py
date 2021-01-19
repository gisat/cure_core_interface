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
    ENDPOINT = '/atom/search/description.xml'
    def get(self):
        mimetype = 'application/xml'
        description = app_containers.description_documents.get('base')
        response = Response(description.document(DescriptionAtomFormat.ENDPOINT, mimetype),
                            mimetype=mimetype, content_type='text/xml; charset=utf-8')
        return response

class DescriptionJsonFormat(MethodResource, Resource):
    ENDPOINT = '/json/search/description.xml'
    def get(self):
        mimetype = 'application/xml'
        description = app_containers.description_documents.get('base')
        response = Response(description.document(DescriptionAtomFormat.ENDPOINT, mimetype),
                            mimetype=mimetype, content_type='text/xml; charset=utf-8')
        return response

@doc(description='Endpoint to acces Mundi CLMS', tags=['Atom'])
@use_kwargs(api_schemas.get('mundi_clms'), location=('json'))
class AtomMundiClms(MethodResource, Resource):
    def get(self):
        request.args['cataloque'] = 'mundi'
        request.args['collection'] = 'clms'
        query = app_containers.request_processor.build_query(request)
        if query.valid:
            query.send_request()
        if query.valid:
            response = Response(query.to_xml(), mimetype='application/xml', content_type='text/xml; charset=utf-8')
            return response

class MundiClmsDescriptionAtomFormat(MethodResource, Resource):
    ENDPOINT = '/mundiclms/atom/search/description.xml'
    def get(self):
        mimetype = 'application/xml'
        description = app_containers.description_documents.get('mundi_clms')
        response = Response(description.document(DescriptionAtomFormat.ENDPOINT, mimetype),
                            mimetype=mimetype, content_type='text/xml; charset=utf-8')
        return response

# instantiace of reource classes
json_format = JsonFormat()
atom_format = AtomFormat()
atommundiclms=AtomMundiClms()

# registration of api
search_api.add_resource(json_format, '/json/search', endpoint=json_format.__class__.__name__.lower())
search_api.add_resource(atom_format, '/atom/search', endpoint=atom_format.__class__.__name__.lower())
search_api.add_resource(atommundiclms, '/mundiclms/atom/search', endpoint=atommundiclms.__class__.__name__.lower())

search_api.add_resource(DescriptionAtomFormat, DescriptionAtomFormat.ENDPOINT, endpoint=DescriptionAtomFormat.__name__.lower())
search_api.add_resource(DescriptionJsonFormat, DescriptionJsonFormat.ENDPOINT, endpoint=DescriptionJsonFormat.__name__.lower())
search_api.add_resource(MundiClmsDescriptionAtomFormat, MundiClmsDescriptionAtomFormat.ENDPOINT,
                        endpoint=MundiClmsDescriptionAtomFormat.__name__.lower())

docs.register(atom_format.__class__, endpoint=atom_format.__class__.__name__.lower())
docs.register(json_format.__class__, endpoint=json_format.__class__.__name__.lower())
docs.register(atommundiclms.__class__, endpoint=atommundiclms.__class__.__name__.lower())


