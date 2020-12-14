from ccsi.search.service.parameters import StringParameter, IntParameter, BBoxParameter, WKTParameter, FloatParameter, \
    DateTimeParameter, OptionParameter
from ccsi.search.service.transform import simple


class Config:
    # registred collection tags, used to identified service endpoint
    COLLECTION_TAGS = ['clms', 'sentinel1', 'sentinel2']

    # registred catalogue tags, used to identified service endpoint
    CATALOGUES_TAGS = ['mundi', 'scihub']

    # temporary / used in request processor
    SERVICE_TAGS = {'collection': COLLECTION_TAGS,
                    'catalogue': CATALOGUES_TAGS}

    # CCSI base api parameters
    SERVICE_PARAMETERS = {'base': [{'name': 'collection', 'typ': OptionParameter, 'transform': simple, 'default':
                                    COLLECTION_TAGS},
                                   {'name': 'catalogue', 'typ': OptionParameter, 'transform': simple, 'default':
                                    CATALOGUES_TAGS},
                                   {'name': 'searchterm', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'product', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'producttype', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'productid', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'custom', 'typ': StringParameter, 'transform': simple},
                                   {'name': 'maxrecords', 'typ': IntParameter, 'transform': simple, 'default': '50'},
                                   {'name': 'page', 'typ': IntParameter, 'transform': simple},
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
                                     {'name': 'rows', 'typ': IntParameter, 'transform': simple, 'default': '50'},
                                     {'name': 'orbitdirection', 'typ': StringParameter, 'transform': simple}]}

    MAPED_PAIRS = {'base': {},
                   'mundi_clms': {'searchterm': 'g',
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
                              'custom:orbitdirection': 'orbitdirection'}}

    XML_NAMESPACES = {'atom': {'prefix': '', 'namespace': 'http://www.w3.org/2005/Atom'},
                      'dc': {'prefix': 'dc', 'namespace': "http://purl.org/dc/elements/1.1/"},
                      'gml': {'prefix': 'gml', 'namespace': 'http://www.opengis.net/gml'},
                      'opensearch': {'prefix': 'opensearch', 'namespace': 'http://a9.com/-/spec/opensearch/1.1/'}}


    ENTRY_MAPED_PAIRS = {'mundi_clms': {'id': ['id', XML_NAMESPACES.get('atom'), 'text'],
                                        'title': ['title', XML_NAMESPACES.get('atom'), 'text'],
                                        'category': ['category', XML_NAMESPACES.get('atom'), 'attribute'],
                                        'link': ['link', XML_NAMESPACES.get('atom'), 'attribute'],
                                        'identifier': ['identifier', XML_NAMESPACES.get('dc'), 'text'],
                                        'date':  ['date', XML_NAMESPACES.get('dc'), 'text'],
                                        'creator': ['creator', XML_NAMESPACES.get('dc'), 'text'],
                                        'geometry': ['*', XML_NAMESPACES.get('gml'), 'geometry'],
                                        'beginPosition': ['beginPosition', XML_NAMESPACES.get('gml'), 'text'],
                                        'endPosition': ['endPosition', XML_NAMESPACES.get('gml'), 'text']},
                         'scihub': {'id': ["@name='uuid'", XML_NAMESPACES.get('atom'), 'text']}}

    ENTRY_PARS = {'id': {'type': 'text', 'namespace': XML_NAMESPACES.get('atom')},
                  'title': {'type': 'text', 'namespace': XML_NAMESPACES.get('atom')},
                  'category': {'type': 'attribute', 'namespace': XML_NAMESPACES.get('atom')},
                  'link': {'type': 'attribute',  'namespace': XML_NAMESPACES.get('atom')},
                  'identifier': {'type': 'text', 'namespace': XML_NAMESPACES.get('dc')},
                  'date': {'type': 'text', 'namespace': XML_NAMESPACES.get('dc')},
                  'creator': {'type': 'text', 'namespace': XML_NAMESPACES.get('dc')},
                  'geometry': {'type': 'geometry', 'namespace': XML_NAMESPACES.get('gml')},
                  'beginPosition': {'type': 'text', 'namespace': XML_NAMESPACES.get('gml')},
                  'endPosition': {'type': 'text', 'namespace': XML_NAMESPACES.get('gml')}}


    SERVICES = {'base': {'base_url': None,
                         'type_query': None,
                         'auth': {'type': None, 'login': None, 'pwd': None},
                         'collection': COLLECTION_TAGS,
                         'catalogue': CATALOGUES_TAGS,
                         'response': {'response_type': None,
                                      'properties': None}
                         },

                'scihub': {'base_url': 'https://scihub.copernicus.eu/dhus/search?q=',
                           'type_query': 'singe_string',
                           'auth': {'type': 'login', 'login': 'mopletal', 'pwd': 'vzZn342CQu3t'},
                           'collection': ['sentinel1', 'sentinel2'],
                           'catalogue': ['scihub'],
                           'response': {'response_type': 'xml',
                                        'properties': {'mapped': ENTRY_MAPED_PAIRS.get('scihub'),
                                                       'entry_tag': 'entry'}}

                           },

                'mundi_clms': {'base_url': 'https://catalog-browse.default.mundiwebservices.com/acdc/catalog/proxy/'
                                           'search/LandMonitoring/opensearch?',
                               'type_query': 'simple',
                               'auth': {'type': None, 'login': None, 'pwd': None},
                               'collection': ['clms'],
                               'catalogue': ['mundi'],
                               'response': {'response_type': 'xml',
                                            'properties': {'mapped': ENTRY_MAPED_PAIRS.get('mundi_clms'),
                                                           'entry_tag': 'entry'}}
                               }
                }

    # hide this in future into evn
    SECRET_KEY = 'dde809d6027c0f55ce89e56fd54703b6'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

