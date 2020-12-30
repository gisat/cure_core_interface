from ccsi.app.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, \
    FloatParameter, DateTimeParameter, OptionParameter
from ccsi.app.search.service.transform import simple, check_min_value


class Config:
    # registred collection tags, used to identified service endpoint
    COLLECTION_TAGS = ['clms', 'sentinel1', 'sentinel2']

    # registred catalogue tags, used to identified service endpoint
    CATALOGUES_TAGS = ['mundi', 'scihub']

    SERVICE_TAGS = {'collection': {'sentinel1': ['scihub', 'creodias_sentinel1'],
                                   'sentinel2': ['scihub'],
                                   'clms': ['mundi_clms']},
                    'catalogue': {'mundi': ['mundi_clms'],
                                  'scihub': ['scihub'],
                                  'creodias': ['creodias_sentinel1']}}


    # CCSI base api parameters
    SERVICE_PARAMETERS = {'base': [{'name': 'collection', 'typ': OptionParameter, 'transform': simple, 'default':
                                    COLLECTION_TAGS},
                                   {'name': 'catalogue', 'typ': OptionParameter, 'transform': simple, 'default':
                                    CATALOGUES_TAGS},
                                   {'name': 'searchterm', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'product', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'producttype', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'productid', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'maxrecords', 'typ': IntParameter, 'transform': simple, 'default': ['50']},
                                   {'name': 'startindex', 'typ': IntParameter, 'transform': simple, 'default': ['0']},
                                   {'name': 'page', 'typ': IntParameter, 'transform': simple, 'default': ['0']},
                                   {'name': 'bbox', 'typ': BBoxParameter, 'transform': simple},
                                   {'name': 'geometry', 'typ': WKTParameter, 'transform': simple},
                                   {'name': 'lat', 'typ': FloatParameter, 'transform': simple},
                                   {'name': 'lon', 'typ': FloatParameter, 'transform': simple},
                                   {'name': 'radius', 'typ': FloatParameter, 'transform': simple},
                                   {'name': 'relation', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'start', 'typ': DateTimeParameter, 'transform': simple},
                                   {'name': 'end', 'typ': DateTimeParameter, 'transform': simple},
                                   {'name': 'sortorder', 'typ': StringParameter, 'transform': simple}],
                          'mundi_clms': [{'name': 'g', 'typ': StringParameter, 'transform': simple},
                                         {'name': 'maxRecords', 'typ': IntParameter, 'transform': simple},
                                         {'name': 'uid', 'typ': StringParameter, 'transform': simple},
                                         {'name': 'bbox', 'typ': BBoxParameter, 'transform': simple},
                                         {'name': 'geometry', 'typ': WKTParameter, 'transform': simple},
                                         {'name': 'lat', 'typ': FloatParameter, 'transform': simple},
                                         {'name': 'lon', 'typ': FloatParameter, 'transform': simple},
                                         {'name': 'radius', 'typ': FloatParameter, 'transform': simple},
                                         {'name': 'title', 'typ': StringParameter, 'transform': simple},
                                         {'name': 'name', 'typ': StringParameter, 'transform': simple}],
                          'scihub': [{'name': '', 'typ': StringParameter, 'transform': simple},
                                     {'name': 'producttype', 'typ': StringParameter, 'transform': simple},
                                     {'name': 'rows', 'typ': IntParameter, 'transform': simple},
                                     {'name': 'start', 'typ': IntParameter, 'transform': simple},
                                     {'name': 'orbitdirection', 'typ': StringParameter, 'transform': simple}],
                          'creodias_sentinel1': [{'name': 'q', 'typ': StringParameter, 'transform': simple},
                                                 {'name': 'page', 'typ': IntParameter, 'transform': simple},
                                                 {'name': 'maxRecords', 'typ': IntParameter, 'transform': simple},
                                                 {'name': 'index', 'typ': IntParameter, 'transform': check_min_value, 'default': ['1']},
                                                 {'name': 'identifier', 'typ': StringParameter, 'transform': simple},
                                                 {'name': 'productType"', 'typ': StringParameter, 'transform': simple}]}

    MAPED_PAIRS = {'mundi_clms': {'searchterm': 'g',
                                  'maxrecords': 'maxRecords',
                                  'productid': 'uid',
                                  'bbox': 'bbox',
                                  'geometry': 'geometry',
                                  'lat': 'lat',
                                  'lon': 'lon',
                                  'radius': 'radius',
                                  'custom:title': 'title',
                                  'custom:name': 'name'},
                   'scihub': {'searchterm': '',
                              'producttype': 'producttype',
                              'maxrecords': 'rows',
                              'startindex': 'start',
                              'custom:orbitdirection': 'orbitdirection'},
                   'creodias_sentinel1': {'searchterm': 'q',
                                          'producttype': 'productType"',
                                          'maxrecords': 'maxRecords',
                                          'startindex': 'index',
                                          'productid': 'identifier'}}

    XML_NAMESPACES = {'atom': {'prefix': '', 'namespace': 'http://www.w3.org/2005/Atom'},
                      'dc': {'prefix': 'dc', 'namespace': "http://purl.org/dc/elements/1.1/"},
                      'gml': {'prefix': 'gml', 'namespace': 'http://www.opengis.net/gml'},
                      'opensearch': {'prefix': 'opensearch', 'namespace': 'http://a9.com/-/spec/opensearch/1.1/'},
                      'dias': {'prefix': 'DIAS', 'namespace': 'http://tas/DIAS'}}


    ENTRY_MAPED_PAIRS = {'mundi_clms': {'id': {'func': 'text',
                                               'properties': ['id', XML_NAMESPACES.get('atom')]},
                                        'title': {'func': 'text',
                                                  'properties': ['title', XML_NAMESPACES.get('atom')]},
                                        'category': {'func': 'attribute',
                                                     'properties': ['category', XML_NAMESPACES.get('atom')]},
                                        'link_enclosure': {'func': 'attribute',
                                                           'properties': ['link[@rel="enclosure"]', XML_NAMESPACES.get('atom')]},
                                        'identifier': {'func': 'text',
                                                       'properties': ['identifier', XML_NAMESPACES.get('dc')]},
                                        'date':  {'func': 'text',
                                                  'properties': ['date', XML_NAMESPACES.get('dc')]},
                                        'creator': {'func': 'text',
                                                    'properties': ['creator', XML_NAMESPACES.get('dc')]},
                                        'geometry': {'func': 'gdal_geom', 'properties': None},
                                        'published': {'func': 'text',
                                                      'properties': ['published', XML_NAMESPACES.get('atom')]},
                                        'status': {'func': 'text',
                                                   'properties': ['onlineStatus', XML_NAMESPACES.get('dias')]}},
                         'scihub': {'id': {'func': 'text',
                                           'properties': ["@name='uuid'", XML_NAMESPACES.get('atom')]},
                                    'title': {'func': 'text',
                                              'properties': ['summary', XML_NAMESPACES.get('atom')]},
                                    'link_enclosure': {'func': 'attribute_del',
                                             'properties': ['link[@href]', XML_NAMESPACES.get('atom'), ['rel']]},
                                    'geometry': {'func': 'gml_geom', 'properties': ["@name='gmlfootprint'", XML_NAMESPACES.get('atom')]},
                                    'status': {'func': 'text',
                                               'properties': ['@name="status"', XML_NAMESPACES.get('atom')]}},
                         'creodias_sentinel1': {'id': {'func': 'text',
                                           'properties': ["title", XML_NAMESPACES.get('atom')]},
                                    'title': {'func': 'text',
                                              'properties': ['summary', XML_NAMESPACES.get('atom')]},
                                    'link_enclosure': {'func': 'attribute',
                                                       'properties': ['link[@rel="enclosure"]', XML_NAMESPACES.get('atom')]},
                                    'geometry': {'func': 'gml_geom', 'properties': ["@name='gmlfootprint'", XML_NAMESPACES.get('atom')]},
                                    'identifier': {'func': 'text', 'properties': ['identifier', XML_NAMESPACES.get('dc')]}}}




    ENTRY_PARS = {'id': {'type': 'text', 'tag': 'id', 'namespace': XML_NAMESPACES.get('atom')},
                  'title': {'type': 'text', 'tag': 'title', 'namespace': XML_NAMESPACES.get('atom')},
                  'category': {'type': 'attribute_many', 'tag': 'category', 'namespace': XML_NAMESPACES.get('atom')},
                  'link_enclosure': {'type': 'attribute', 'tag': 'link', 'attrib': {'rel': 'enclosure'},
                           'namespace': XML_NAMESPACES.get('atom')},
                  'identifier': {'type': 'text', 'tag': 'identifier', 'namespace': XML_NAMESPACES.get('dc')},
                  'date': {'type': 'text', 'tag': 'date', 'namespace': XML_NAMESPACES.get('dc')},
                  'creator': {'type': 'text', 'tag': 'creator', 'namespace': XML_NAMESPACES.get('dc')},
                  'geometry': {'type': 'geometry', 'tag': 'geometry', 'namespace': XML_NAMESPACES.get('gml')},
                  'published': {'type': 'text', 'tag': 'published', 'namespace': XML_NAMESPACES.get('atom')},
                  'status': {'type': 'text', 'tag': 'status', 'namespace': XML_NAMESPACES.get('atom')}}

    # hide this in future into evn
    SECRET_KEY = 'dde809d6027c0f55ce89e56fd54703b6'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


    # new
    SERVICES_ = ['scihub', 'mundi_clms', 'creodias_sentinel1']

    CONNECTION_ = {'scihub': {'base_url': 'https://scihub.copernicus.eu/dhus/search?',
                              'type_query': 'scihub_query_rule',
                              'auth': {'type': 'login', 'login': 'mopletal', 'pwd': 'vzZn342CQu3t'}},
                   'mundi_clms': {'base_url': 'https://catalog-browse.default.mundiwebservices.com/acdc/catalog/proxy/'
                                              'search/LandMonitoring/opensearch?',
                                  'type_query': 'simple_encode',
                                  'auth': None},
                   'creodias_sentinel1': {'base_url': 'https://finder.creodias.eu/resto/api/collections/Sentinel1/search.atom?',
                                  'type_query': 'simple_encode',
                                  'auth': None},
                   }

    RESPONSE_PARSERS_ = {'scihub': {'parser_type': 'xml',
                                    'properties': {'mapped_pars': ENTRY_MAPED_PAIRS.get('scihub'),
                                                  'entry_tag': 'entry'}},
                         'mundi_clms': {'parser_type': 'xml_gdal',
                                        'properties': {'mapped_pars': ENTRY_MAPED_PAIRS.get('mundi_clms'),
                                                       'entry_tag': 'entry'}},
                         'creodias_sentinel1': {'parser_type': 'xml_gdal',
                                        'properties': {'mapped_pars': ENTRY_MAPED_PAIRS.get('creodias_sentinel1'),
                                                       'entry_tag': 'entry'}}}


config = Config()
