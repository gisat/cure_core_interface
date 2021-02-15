from ccsi.app.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, \
    FloatParameter, DateTimeParameter, OptionParameter
from ccsi.app.search.service.transform import simple, check_min_value
from ccsi.tmp import XML_NAMESPACES

class Base:
    """temporary resource configuration template"""

    COLLECTION_TAGS = ['clms', 'sentinel1', 'sentinel2', 'sentinel3']

    # registred catalogue tags, used to identified service endpoint
    RESOUCES_TAGS = ['mundi', 'scihub']

    SERVICE_TAGS = {'collection': {'sentinel1': ['scihub', 'creodias_sentinel1', 'mundi_s1'],
                                   'sentinel2': ['scihub', 'mundi_s2'],
                                   'sentinel3': ['mundi_s3'],
                                   'clms': ['mundi_clms']},
                    'resource': {'mundi': ['mundi_clms', 'mundi_s1', 'mundi_s2', 'mundi_s3'],
                                 'scihub': ['scihub'],
                                 'creodias': ['creodias_sentinel1']}}

    RESPONSE_PARSER = None

    ENTRY_SETTING = None

    MAPPED_PAIRS = None

    SERVICE_PARAMETERS = [{'name': 'collection', 'typ': OptionParameter, 'transform': simple, 'default': COLLECTION_TAGS},
                          {'name': 'resource', 'typ': OptionParameter, 'transform': simple, 'default': RESOUCES_TAGS},
                          {'name': 'searchterm', 'typ': StringParameter, 'transform': simple},
                          {'name': 'productid', 'typ': StringParameter, 'transform': simple},
                          {'name': 'maxrecords', 'typ': IntParameter, 'transform': simple, 'default': ['50']},
                          {'name': 'startindex', 'typ': IntParameter, 'transform': simple, 'default': ['1']},
                          {'name': 'page', 'typ': IntParameter, 'transform': simple, 'default': ['0']},
                          {'name': 'bbox', 'typ': BBoxParameter, 'transform': simple},
                          {'name': 'geometry', 'typ': WKTParameter, 'transform': simple},
                          {'name': 'lat', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'lon', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'radius', 'typ': FloatParameter, 'transform': simple},
                          {'name': 'timestart', 'typ': DateTimeParameter, 'transform': simple},
                          {'name': 'timeend', 'typ': DateTimeParameter, 'transform': simple}]

    CONNECTION = None

    ENDPOINT = {'properties': {'service_name': 'base',
                               'collection': None,
                               'resource': None},
                'description': {'swagger_desc': 'General endpoint to access all registred datasets',
                                'api_schema': 'base',
                                'tag': ['global']}}
