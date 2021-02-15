from ccsi.app.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, \
    FloatParameter, DateTimeParameter, OptionParameter
from ccsi.app.search.service.transform import simple, check_min_value
from ccsi.tmp import XML_NAMESPACES

class Scihub:
    """temporary resource configuration template"""

    RESPONSE_PARSER = {'parser_type': 'xml'}

    ENTRY_SETTING = None

    MAPPED_PAIRS = {'searchterm': '',
                    'producttype': 'producttype',
                    'maxrecords': 'rows',
                    'startindex': 'start',
                    'orbitdirection': 'orbitdirection'}

    SERVICE_PARAMETERS = [{'name': '', 'typ': StringParameter, 'transform': simple},
                          {'name': 'producttype', 'typ': StringParameter, 'transform': simple},
                          {'name': 'rows', 'typ': IntParameter, 'transform': simple},
                          {'name': 'start', 'typ': IntParameter, 'transform': simple},
                          {'name': 'orbitdirection', 'typ': StringParameter, 'transform': simple}]

    CONNECTION = {'base_url': 'https://scihub.copernicus.eu/dhus/search?',
                  'type_query': 'scihub_query_rule',
                  'auth': {'type': 'login', 'login': 'mopletal', 'pwd': 'vzZn342CQu3t'}}

    ENDPOINT = None
