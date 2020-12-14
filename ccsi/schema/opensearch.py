from ccsi.config import Config
from lxml.etree import Element, SubElement
from urllib.parse import urlencode
from datetime import datetime


class OpenSearchResponse:

    # def request_args
    #
    # def qurey_link(self, request_args, start_index):
    #     requestargs =
    #
    #     return {'role': 'request', 'searchTerms': requestargs, startPage': start_index}}


    def nsmap(self):
        """return xml namespaces in for required by lxml"""
        return {(item.get('prefix') if item.get('prefix') != '' else None): item.get('namespace')
                for item in Config.XML_NAMESPACES.values()}

    @staticmethod
    def create_SubElement(parent, tag, attrib={}, text=None, nsmap=None, **_extra):
        result = SubElement(parent, tag, attrib, nsmap, **_extra)
        result.text = text
        return result

    def atom_head(self, request_args, n_entry, url, start_index, maxrecords):
        feed = Element('feed', nsmap=self.nsmap())
        title = self.create_SubElement(feed, 'title', text=f'Copernicus Core Service Interface search results for:'
                                                           f'{urlencode(request_args)}')
        subtitle = self.create_SubElement(feed, 'subtitle', text=f'Displaying {n_entry} results')
        updated = self.create_SubElement(feed, 'updated', text=datetime.now().isoformat())
        author = self.create_SubElement(feed, 'author')
        name = self.create_SubElement(author, 'name', text='Copernicus Core Service Interface')
        id = self.create_SubElement(feed, 'id', text=url)
        totalresults = self.create_SubElement(feed, 'totalResults', text=n_entry)
        startindex = self.create_SubElement(feed, 'startIndex', text=start_index)
        itemsperpage = self.create_SubElement(feed, 'itemsPerPage', text=maxrecords)
        query = self.create_SubElement(feed, 'Query', attrib={'role': 'request', 'searchTerms': urlencode(request_args),
                                                              'startPage': start_index})
        search_link = self.create_SubElement(feed, 'link', attrib={'rel': 'search',
                                                                   'type': 'application/opensearchdescription+xml',
                                                                   'href': 'desxcription.xml'})
        self_link = self.create_SubElement(feed, 'link', attrib={'rel': 'self',
                                                                   'type': 'application/atom+xml',
                                                                   'href': url})
        return feed

    def json_head(self, request_args, n_entry, url, start_index, maxrecords):
        properties = {
            "id": "79a425b8-ca6d-522a-b8ef-e7b93217b413",
            "totalResults": 1589664,
            "exactCount": True if maxrecords >= n_entry else True,
            "startIndex": start_index,
            "itemsPerPage": int(maxrecords),
            "query": request_args,
            "links": [
                {
                    "rel": "self",
                    "type": "application/json",
                    "title": "self",
                    "href": "https://finder.creodias.eu/resto/api/collections/Sentinel1/search.json?&productType=GRD&orbitnumber=18"
                },
                {
                    "rel": "search",
                    "type": "application/opensearchdescription+xml",
                    "title": "OpenSearch Description Document",
                    "href": "https://finder.creodias.eu/resto/api/collections/Sentinel1/describe.xml"
                },
                {
                    "rel": "next",
                    "type": "application/json",
                    "title": "next",
                    "href": "https://finder.creodias.eu/resto/api/collections/Sentinel1/search.json?&productType=GRD&orbitnumber=18&page=2"
                },
                {
                    "rel": "last",
                    "type": "application/json",
                    "title": "last",
                    "href": "https://finder.creodias.eu/resto/api/collections/Sentinel1/search.json?&productType=GRD&orbitnumber=18&page=79484"
                }
            ]
        }
        pass

open_search_response = OpenSearchResponse()