from ccsi.app.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, \
    FloatParameter, DateTimeParameter, OptionParameter
from ccsi.app.search.service.transform import simple, check_min_value

# TODO: transfer config into DB, generation and registration of parameters

class Config:

    VERSION = '0.8'
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

    XML_NAMESPACES = {'atom': {'prefix': '', 'namespace': 'http://www.w3.org/2005/Atom'},
                      'dc': {'prefix': 'dc', 'namespace': "http://purl.org/dc/elements/1.1/"},
                      'gml': {'prefix': 'gml', 'namespace': 'http://www.opengis.net/gml'},
                      'opensearch': {'prefix': 'opensearch', 'namespace': 'http://a9.com/-/spec/opensearch/1.1/'},
                      'dias': {'prefix': 'DIAS', 'namespace': 'http://tas/DIAS'},
                      'geo': {'prefix': 'geo', 'namespace': 'http://a9.com/-/opensearch/extensions/geo/1.0/'},
                      'time': {'prefix': 'time', 'namespace': 'http://a9.com/-/opensearch/extensions/time/1.0/'},
                      'param': {'prefix': 'param', 'namespace':  'http://a9.com/-/spec/opensearch/extensions/parameters/1.0/'},
                      'ccsi': {'prefix': 'param', 'namespace':  'http://spec/ccsi/parameters'},
                      'eo': {'prefix': 'param', 'namespace':  'http://a9.com/-/opensearch/extensions/eo/1.0/'}}

    PARAMETERS_DESCRIPTION = {'collection': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Data collection name'},
                              'cataloque': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Name of the data catalogue'},
                              'searchterm': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'General queryable parameters'},
                              'producttype': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Product type'},
                              'productid': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Cataloque specific id of the product'},
                              'maxrecords': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'Number of records per page'},
                              'startindex': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'Start index o results'},
                              'page': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'Page of results; default 0'},
                              'bbox': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Region of Interest defined by 'west, south, east, north' coordinates of longitude, latitude, in decimal degrees (EPSG:4326)"},
                              'geometry': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Region of Interest defined in Well Known Text standard (WKT) with coordinates in decimal degrees (EPSG:4326)"},
                              'lat': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Longitude expressed in decimal degrees (EPSG:4326) - have to be used with geo:lat and geo:radius"},
                              'lon': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Longitude expressed in decimal degrees (EPSG:4326) - have to be used with geo:lon and geo:radius"},
                              'radius': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Expressed in meters - should be used with geo:lon and geo:lat"},
                              'start': {'namespace': XML_NAMESPACES.get('time'), 'title': 'Search interval start time'},
                              'end': {'namespace': XML_NAMESPACES.get('time'), 'title': 'Search interval end time'},
                              'custom:title': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Custom parameter availible of certaint catalogues'},
                              'custom:name': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Custom parameter availible of certaint catalogues'},
                              'custom:orbitdirection': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Custom parameter availible of certaint catalogues'}
                              }

    # CCSI base api parameters
    SERVICE_PARAMETERS = {'base': [{'name': 'collection', 'typ': OptionParameter, 'transform': simple, 'default': COLLECTION_TAGS},
                                   {'name': 'catalogue', 'typ': OptionParameter, 'transform': simple, 'default': CATALOGUES_TAGS},
                                   {'name': 'searchterm', 'typ': StringParameter, 'transform': simple},
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
                                   {'name': 'start', 'typ': DateTimeParameter, 'transform': simple},
                                   {'name': 'end', 'typ': DateTimeParameter, 'transform': simple}],
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
