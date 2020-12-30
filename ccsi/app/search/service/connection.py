from ccsi.utils import import_from
from requests import get
from requests.auth import HTTPBasicAuth
from collections import OrderedDict

# TODO: make servicebuilder.registr method, connection to db
#


class Connection:
    """Class represents each registered service. Its base url, parameters, auth etc."""

    def __init__(self, base_url, type_query, auth):
        self._base_url = base_url
        self._type_query = type_query
        self._auth = self._get_auth(auth)

    @classmethod
    def create(cls, base_url, type_query, auth, **ignore):
        return Connection(base_url, type_query, auth)

    def send_request(self, query: dict):
        """
        sending the request to original service
        query - dict contain original parameters of service
        """
        response = self.connection(query)
        if response.status_code != 200:
            return
        return response

    @staticmethod
    def _get_auth(auth):
        if auth is None:
            return None
        elif auth.get('type') == 'login':
            return HTTPBasicAuth(auth.get('login'), auth.get('pwd'))
        else:
            raise ValueError(f'Unsupported login type: {auth.get("type")}')

    def _connect_without_auth(self, query):
        return get(self._base_url, params=query)

    def _get_query_string(self, query):
        query = OrderedDict(sorted(query.items(), key=lambda t: len(t[0])))
        params = import_from('ccsi.app.search.service.transform', self._type_query)(query)
        return self._base_url + params

    def connection(self, query):
        url = self._get_query_string(query)
        return get(url, auth=self._auth)





