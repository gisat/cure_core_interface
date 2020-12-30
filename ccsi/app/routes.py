from flask import Blueprint, Response
from flask import request as request
from ccsi.containers import app_containers

search = Blueprint('search', __name__)


@search.route('/json/search', methods=['GET'])
def json():
    query = app_containers.request_processor.build_query(request)
    if query.valid:
        query.send_request()
    if query.valid:
        response = Response(query.to_json(), mimetype='application/json')
        response.headers["Content-Type"] = 'application/json; charset=utf-8'
        return response


@search.route('/atom/search', methods=['GET'])
def atom():
    query = app_containers.request_processor.build_query(request)
    if query.valid:
        query.send_request()
    if query.valid:
        response = Response(query.to_xml(), mimetype='application/xml')
        response.headers["Content-Type"] = 'text/xml; charset=utf-8'
        return response

