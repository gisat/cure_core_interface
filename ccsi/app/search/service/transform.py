from collections import OrderedDict
from urllib.parse import urlencode
# parameters transformation function
def simple(self, value):
    return value

def check_min_value(self, value):
    if int(value) < int(self.default[0]):
        return int(self.default[0])
    return value

# request transformation function
def simple_encode(query):
    return urlencode(query)

def scihub_query_rule(query):
    new_query = OrderedDict({key: query.pop(key) for key in ['rows','start']})
    params = urlencode(new_query) + '&q=' + urlencode(query)
    return params








