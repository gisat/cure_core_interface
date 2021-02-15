from ccsi.tmp import XML_NAMESPACES, MundiCLMS, MundiS1, MundiS2, MundiS3, CreodiasS1, CreodiasS2, CreodiasS3, Scihub, \
    Base

# TODO: transfer config into DB, generation and registration of parameters
# TODO: harmonization of custom:status mundi vs credias
# TODO: harmonization of platform mundi vs credias
# TODO: harmonization of senzormode mundi vs credias

PSEUDO_DB = {'base': Base,
             'mundi_clms': MundiCLMS,
             'mundi_s1': MundiS1,
             'mundi_s2': MundiS2,
             'mundi_s3': MundiS3,
             'scihub': Scihub,
             'creodias_s1': CreodiasS1,
             'creodias_s2': CreodiasS2,
             'creodias_s3': CreodiasS3}


class Config:

    VERSION = '0.8'

    # registred collection tags, used to identified service endpoint
    COLLECTION_TAGS = ['clms', 'sentinel1', 'sentinel2', 'sentinel3']

    # registred catalogue tags, used to identified service endpoint
    RESOUCES_TAGS = ['mundi', 'scihub', 'creodias']

    SERVICE_TAGS = {'collection': {'sentinel1': ['scihub', 'creodias_sentinel1', 'mundi_s1'],
                                   'sentinel2': ['scihub', 'mundi_s2'],
                                   'sentinel3': ['mundi_s3'],
                                   'clms': ['mundi_clms']},
                    'resource': {'mundi': ['mundi_clms', 'mundi_s1', 'mundi_s2', 'mundi_s3'],
                                  'scihub': ['scihub'],
                                  'creodias': ['creodias_s1', 'creodias_s2', 'creodias_s3' ]}}

    PARAMETERS_DESCRIPTION = {'collection': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Data collection name'},
                              'resource': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Name of the data resourses'},
                              'searchterm': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'General queryable parameters'},
                              'productid': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Product id of the product'},
                              'maxrecords': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'Number of records per page'},
                              'startindex': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'Start index o results'},
                              'page': {'namespace': XML_NAMESPACES.get('opensearch'), 'title': 'Page of results; default 0'},
                              'bbox': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Region of Interest defined by 'west, south, east, north' coordinates of longitude, latitude, in decimal degrees (EPSG:4326)"},
                              'geometry': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Region of Interest defined in Well Known Text standard (WKT) with coordinates in decimal degrees (EPSG:4326)"},
                              'lat': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Longitude expressed in decimal degrees (EPSG:4326) - have to be used with geo:lat and geo:radius"},
                              'lon': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Longitude expressed in decimal degrees (EPSG:4326) - have to be used with geo:lon and geo:radius"},
                              'radius': {'namespace': XML_NAMESPACES.get('geo'), 'title': "Expressed in meters - should be used with geo:lon and geo:lat"},
                              'timestart': {'namespace': XML_NAMESPACES.get('time'), 'title': 'Search interval start time'},
                              'timeend': {'namespace': XML_NAMESPACES.get('time'), 'title': 'Search interval end time'},
                              'custom:title': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Custom parameter availible of certaint resourcess'},
                              'custom:name': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Geoname location intersecting product footprint'},
                              'orbitdirection': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Acquisition orbit direction'},
                              'platform': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Platform collection'},
                              'producttype': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Type of the product'},
                              'resolution': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Product resolution'},
                              'customm:status': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product on-line status'},
                              'instrument': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Instrument name'},
                              'sensortype': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Sensor type'},
                              'sensormode': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Sensor mode'},
                              'acquisition': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Acquisition mission mode'},
                              'polarisation': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Polarisation channel(s) configuration'},
                              'processinglevel': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Product processing level'},
                              'custom:quality': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product quality check status'},
                              'acquisitionstation': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Acquisition station'},
                              'orbitnumber': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Acquisition orbit number'},
                              'cloudcover': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Product cloud coverage percentage interval'},
                              'snowcover': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Product snow coverage percentage interval'},
                              'organisationName': {'namespace': XML_NAMESPACES.get('eo'), 'title': 'Name of the organization'},
                              'custom:cultivatedcover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product cultivated coverage percentage interval'},
                              'custom:desertcover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product desert coverage percentage interval'},
                              'custom:floodedcover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product flood coverage percentage interval'},
                              'custom:forestcover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product forest coverage percentage interval'},
                              'custom:herbaceouscover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product herbal coverage percentage interval'},
                              'custom:icecover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product ice coverage percentage interval'},
                              'custom:urbancover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product urban coverage percentage interval'},
                              'custom:watercover': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product water coverage percentage interval'},
                              'custom:relativeorbitnumber': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product relative orbit number'},
                              'custom:inspitre_identifier': {'namespace': XML_NAMESPACES.get('ccsi'), 'title': 'Product product inspire identificator'}
                              }

    # active resources
    SERVICES = ['mundi_clms', 'mundi_s1', 'mundi_s2', 'mundi_s3']

    # CCSI base api parameters

    SERVICE_PARAMETERS = {service_name: PSEUDO_DB.get(service_name).SERVICE_PARAMETERS for service_name in SERVICES}
    SERVICE_PARAMETERS.update({'base': PSEUDO_DB.get('base').SERVICE_PARAMETERS})
    MAPPED_PAIRS = {service_name: PSEUDO_DB.get(service_name).MAPPED_PAIRS for service_name in SERVICES}
    ENTRY_MAPPED_PAIRS = {service_name: PSEUDO_DB.get(service_name).ENTRY_SETTING for service_name in SERVICES}
    CONNECTION = {service_name: PSEUDO_DB.get(service_name).CONNECTION for service_name in SERVICES}
    RESPONSE_PARSER = {service_name: PSEUDO_DB.get(service_name).RESPONSE_PARSER for service_name in SERVICES}
    ENDPOINTS = [PSEUDO_DB.get(service_name).ENDPOINT for service_name in SERVICES]
    ENDPOINTS.append(PSEUDO_DB.get('base').ENDPOINT)
    SHORT_NAME = {service_name: PSEUDO_DB.get(service_name).SHORT_NAME for service_name in SERVICES}

    ENTRY_PARS = {'uid': {'type': 'text', 'tag': 'uid', 'namespace': XML_NAMESPACES.get('atom')},
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

config = Config()
