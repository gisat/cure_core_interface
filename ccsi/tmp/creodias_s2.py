from ccsi.app.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, \
    FloatParameter, DateTimeParameter, OptionParameter
from ccsi.app.search.service.transform import simple, check_min_value
from ccsi.tmp import XML_NAMESPACES

class CreodiasS2:
    """temporary resource configuration template"""

    RESPONSE_PARSER = {'parser_type': 'xml_gdal'}

    ENTRY_SETTING = None

    MAPPED_PAIRS = {'searchterm': 'q',
                    'maxrecords': 'maxRecords',
                    'startindex': 'index',
                    'productid': 'parentIdentifier',
                    'geometry': 'geometry',
                    'bbox': 'box',
                    'custom:name': 'name',
                    'lat': 'lat',
                    'lon': 'lon',
                    'radius': 'radius',
                    'timestart': 'startDate',
                    'timeend': 'completionDate',
                    'producttype': 'productType',
                    'level': 'processingLevel',
                    'platform': 'platform',
                    'instrumet': 'instrument',
                    'resolution': 'resolution',
                    'organisationName': 'organisationName',
                    'orbitnumber': 'orbitNumber',
                    'sensormode': 'sensorMode',
                    'cloudcover': 'cloudCover',
                    'snowcover': 'snowCover',
                    'custom:cultivatedover': 'cultivatedCover',
                    'custom:desertcover': 'desertCover',
                    'custom:floodedcover': 'floodedCover',
                    'custom:forestcover': 'forestCover',
                    'custom:herbaceouscover': 'herbaceousCover',
                    'custom:icecover': 'iceCover',
                    'custom:urbancover': 'urbanCover',
                    'custom:waterCover': 'waterCover',
                    'custom:status': 'status',
                    'orbitdirection': 'orbitDirection',
                    'custom:relativeorbitnumber': 'relativeOrbitNumber'}

    SERVICE_PARAMETERS = [{'name': 'q', 'typ': StringParameter, 'transform': simple},
                          {'name': 'maxRecords', 'typ': IntParameter, 'transform': simple},
                          {'name': 'index', 'typ': IntParameter, 'transform': check_min_value, 'default': ['1']},
                          {'name': 'page', 'typ': IntParameter, 'transform': simple, 'default': ['1']},
                          {'name': 'parentIdentifier', 'typ': StringParameter, 'transform': simple},
                          {'name': 'geometry', 'typ': WKTParameter, 'transform': simple},
                          {'name': 'box', 'typ': BBoxParameter, 'transform': simple},
                          {'name': 'name', 'typ': StringParameter, 'transform': simple},
                          {'name': 'lat', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'lon', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'radius', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'startDate', 'typ': DateTimeParameter, 'transform': simple},
                          {'name': 'completionDate', 'typ': DateTimeParameter, 'transform': simple},
                          {'name': 'productType', 'typ': StringParameter, 'transform': simple},
                          {'name': 'processingLevel', 'typ': StringParameter, 'transform': simple},
                          {'name': 'platform', 'typ': StringParameter, 'transform': simple},
                          {'name': 'instrument', 'typ': StringParameter, 'transform': simple},
                          {'name': 'resolution', 'typ': IntParameter, 'transform': simple},
                          {'name': 'organisationName', 'typ': StringParameter, 'transform': simple},
                          {'name': 'orbitNumber', 'typ': IntParameter, 'transform': simple},
                          {'name': 'sensorMode', 'typ': StringParameter, 'transform': simple},
                          {'name': 'cloudCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'snowCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'cultivatedCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'desertCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'floodedCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'forestCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'herbaceousCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'iceCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'urbanCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'waterCover', 'typ': IntParameter, 'transform': simple},
                          {'name': 'status', 'typ': StringParameter, 'transform': simple},
                          {'name': 'orbitDirection', 'typ': StringParameter, 'transform': simple},
                          {'name': 'relativeOrbitNumber', 'typ': IntParameter, 'transform': simple}]

    CONNECTION = {'base_url': 'https://finder.creodias.eu/resto/api/collections/Sentinel3/search.atom?',
                  'type_query': 'simple_encode',
                  'auth': None}

    ENDPOINT = {'properties': {'service_name': 'creodias_s2',
                               'collection': 'sentinel1',
                               'resource': None},
                'description': {'swagger_desc': 'General endpoint to access products from Creodias Sentinel 2',
                                'api_schema': 'creodias_s2',
                                'tag': ['Creodias']}}