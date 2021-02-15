# TODO: Temporary, all configuration will be move into DB
XML_NAMESPACES = {'atom': {'atom': 'http://www.w3.org/2005/Atom'},
                  'dc': {'dc': 'http://purl.org/dc/elements/1.1/'},
                  'gml': {'gml': 'http://www.opengis.net/gml'},
                  'opensearch': {'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'},
                  'dias': {'DIAS': 'http://tas/DIAS'},
                  'geo': {'geo': 'http://a9.com/-/opensearch/extensions/geo/1.0/'},
                  'time': {'time': 'http://a9.com/-/opensearch/extensions/time/1.0/'},
                  'param': {'param': 'http://a9.com/-/spec/opensearch/extensions/parameters/1.0/'},
                  'ccsi': {'ccsi': 'http://spec/ccsi/parameters'},
                  'eo': {'eo': 'http://a9.com/-/spec/opensearch/extensions/eo/1.0/'},
                  'georss': {'georss': 'http://www.georss.org/georss'}}

from ccsi.tmp.mundi_clms import MundiCLMS
from ccsi.tmp.mundi_s1 import MundiS1
from ccsi.tmp.mundi_s2 import MundiS2
from ccsi.tmp.mundi_s3 import MundiS3
from ccsi.tmp.creodias_s1 import CreodiasS1
from ccsi.tmp.creodias_s2 import CreodiasS2
from ccsi.tmp.creodias_s3 import CreodiasS3
from ccsi.tmp.base import Base
from ccsi.tmp.scihub import Scihub


# class Template:
#     """temporary resource configuration template"""
#
#     RESPONSE_PARSER = None
#
#     ENTRY_SETTING = None
#
#     MAPPED_PAIRS = None
#
#     SERVICE_PARAMETERS = None
#
#     CONNECTION = None
#
#     ENDPOINT = None
