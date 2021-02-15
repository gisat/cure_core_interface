from ccsi.app.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, \
    FloatParameter, DateTimeParameter, OptionParameter
from ccsi.app.search.service.transform import simple, check_min_value
from ccsi.tmp import XML_NAMESPACES


class MundiS2:
    """temporary resource configuration template"""

    RESPONSE_PARSER = {'parser_type': 'xml_gdal'}

    ENTRY_SETTING = {'uid': {'typ': 'text',
                             'tag': {'tag': 'uid', 'namespace': XML_NAMESPACES.get('atom')},
                             'parser': {'type': 'xml',
                                        'properties': {'func': 'text', 'xpath': 'atom:id', 'namespace': XML_NAMESPACES.get('atom')}}
                             },
                     'summary': {'typ': 'text',
                                 'tag': {'tag': 'summary', 'namespace': XML_NAMESPACES.get('atom')},
                                 'parser': {'type': 'xml',
                                            'properties': {'func': 'text', 'xpath': 'atom:summary', 'namespace': XML_NAMESPACES.get('atom')}}
                                 },
                     'category': {'typ': 'attribute_many',
                                  'tag': {'tag': 'category', 'namespace': XML_NAMESPACES.get('atom')},
                                  'parser': {'type': 'xml',
                                             'properties': {'func': 'attribute', 'xpath': 'atom:category', 'namespace': XML_NAMESPACES.get('atom')}}},
                     'geometry': {'typ': 'geometry',
                                  'tag': {'tag': 'geometry', 'namespace': XML_NAMESPACES.get('atom')},
                                  'parser': {'type': 'xml',
                                             'properties': {'func': 'gdal_geom', 'xpath': 'georss:where', 'namespace': XML_NAMESPACES.get('georss')}}},
                     'status': {'typ': 'text',
                                'tag': {'tag': 'status', 'namespace': XML_NAMESPACES.get('ccsi')},
                                'parser': {'type': 'xml',
                                           'properties': {'func': 'text', 'xpath': 'DIAS:onlineStatus', 'namespace': XML_NAMESPACES.get('dias')}}},
                     'published': {'typ': 'text',
                                   'tag': {'tag': 'published', 'namespace': XML_NAMESPACES.get('atom')},
                                   'parser': {'type': 'xml',
                                              'properties': {'func': 'text', 'xpath': 'atom:published', 'namespace': XML_NAMESPACES.get('atom')}}},
                     'resolution': {'typ': 'text',
                                    'tag': {'tag': 'resolution', 'namespace': XML_NAMESPACES.get('eo')},
                                    'parser': {'type': 'xml',
                                               'properties': {'func': 'text', 'find': '{http://a9.com/-/spec/opensearch/extensions/eo/1.0/}resolution'}}},
                     'link_enclosure': {'typ': 'attribute',
                                        'tag': {'tag': 'link', 'attrib': {'rel': 'enclosure'},  'namespace': XML_NAMESPACES.get('atom')},
                                        'parser': {'type': 'xml',
                                                   'properties': {'func': 'enclousure_from_text', 'findall': '{http://tas/DIAS}imagePatternURI'}}}
                     }

    MAPPED_PAIRS = {'searchterm': 'g',
                    'custom:title': 'title',
                    'startindex': 'startIndex',
                    'maxrecords': 'maxRecords',
                    'productid': 'parentIdentifier',
                    'bbox': 'bbox',
                    'geometry': 'geometry',
                    'lat': 'lat',
                    'lon': 'lon',
                    'radius': 'radius',
                    'custom:name': 'name',
                    'timestart': 'timeStart',
                    'timeend': 'timeEnd',
                    'platform': 'platform',
                    'instrumet': 'instrument',
                    'sensortype': 'sensorType',
                    'sensormode': 'sensorMode',
                    'orbitdirection': 'orbitDirection',
                    'acquisition': 'acquisitionType',
                    'producttype': 'productType',
                    'level': 'processingLevel',
                    'custom:quality': 'productQualityStatus',
                    'custom:status': 'onlineStatus',
                    'resolution': 'resolution',
                    'cloudcover': 'cloudCover',
                    'snowcover': 'snowCover',
                    'acquisitionstation': 'acquisitionStation',
                    'orbitnumber': 'orbitNumber'}

    SERVICE_PARAMETERS = [{'name': 'g', 'typ': StringParameter, 'transform': simple},
                          {'name': 'title', 'typ': StringParameter, 'transform': simple},
                          {'name': 'startIndex', 'typ': IntParameter, 'transform': simple},
                          {'name': 'maxRecords', 'typ': IntParameter, 'transform': simple},
                          {'name': 'parentIdentifier', 'typ': StringParameter, 'transform': simple},
                          {'name': 'bbox', 'typ': BBoxParameter, 'transform': simple},
                          {'name': 'geometry', 'typ': WKTParameter, 'transform': simple},
                          {'name': 'lat', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'lon', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'radius', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'name', 'typ': StringParameter, 'transform': simple},
                          {'name': 'timeStart', 'typ': DateTimeParameter, 'transform': simple},
                          {'name': 'timeEnd', 'typ': DateTimeParameter, 'transform': simple},
                          {'name': 'platform', 'typ': StringParameter, 'transform': simple},
                          {'name': 'instrument', 'typ': StringParameter, 'transform': simple},
                          {'name': 'sensorType', 'typ': StringParameter, 'transform': simple},
                          {'name': 'sensorMode', 'typ': StringParameter, 'transform': simple},
                          {'name': 'orbitDirection', 'typ': StringParameter, 'transform': simple},
                          {'name': 'acquisitionType', 'typ': StringParameter, 'transform': simple},
                          {'name': 'productType', 'typ': StringParameter, 'transform': simple},
                          {'name': 'processingLevel', 'typ': StringParameter, 'transform': simple},
                          {'name': 'productQualityStatus', 'typ': StringParameter, 'transform': simple},
                          {'name': 'onlineStatus', 'typ': StringParameter, 'transform': simple},
                          {'name': 'resolution', 'typ': IntParameter, 'transform': simple},
                          {'name': 'cloudCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'snowCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'acquisitionStation', 'typ': StringParameter, 'transform': simple},
                          {'name': 'orbitNumber', 'typ': IntParameter, 'transform': simple}]

    CONNECTION = {'base_url': 'https://catalog-browse.default.mundiwebservices.com/acdc/catalog/proxy/'
                              'search/Sentinel2/opensearch?',
                  'type_query': 'simple_encode',
                  'auth': None}

    SHORT_NAME = 'Mundi Sentinel 2 endpoint'

    ENDPOINT = {'properties': {'service_name': 'mundi_s2',
                               'collection': 'sentinel2',
                               'resource': 'mundi'},
                'description': {'swagger_desc': 'General endpoint to access products from Mundi Sentinel 2',
                                'api_schema': 'mundi_s2',
                                'tag': ['Mundi']}}
