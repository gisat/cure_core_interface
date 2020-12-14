from flask import Blueprint, jsonify, Response
from flask import request as frequest
from ccsi.search.main import request_processor

search = Blueprint('search', __name__)


@search.route('/json/search', methods=['GET'])
def json():
    # query = request_processor.build_query(request.args.copy())
    # if query.valid:
    #     query.send_request()

    # if query.valid:
    return jsonify((frequest.url, frequest.base_url, frequest.args))


@search.route('/atom/search', methods=['GET'])
def atom():
    query = request_processor.build_query()
    if query.valid:
        query.send_request()

    if query.valid:
        response = Response(query.to_xml(), mimetype='application/xml')
        response.headers["Content-Type"] = 'text/xml; charset=utf-8'
        return response

