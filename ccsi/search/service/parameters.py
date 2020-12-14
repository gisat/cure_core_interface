from shapely import wkt, errors
from shapely.geometry import box
from dateutil.parser import isoparse
import types


class Parameter:
    """Base class represent parameter type. Take name, type of parameter (str, int etc.), take error message and
    transformation function i.e. how the input value or parameter name is transformed from base api to service api """

    def __init__(self, name, param_type, error, transform, selection=[], default=None):
        """
        name        - name of the parameter
        typ         - type of parameter
        error       - error message if value is not validated
        transform   - transformation function that transform input form into form expected by target endpoint
        value       - expected values i.e all options, default empty list means any valid value is expected
        default     - defalut value
        """
        self._name = name
        self._param_type = param_type
        self._error = error
        self._default = default
        self._selection = selection
        setattr(self, '_transform', types.MethodType(transform, self))

    @property
    def default(self):
        return self._default

    @property
    def default(self):
        return self._default

    def validate(self, value):
        if not self._isinstance(value):
            return self._error_msg(value)
        return True

    def _error_msg(self, value):
        return f'Parameter {self._name} should be {self._error}. Input value is {value}'

    def _isinstance(self, value):
        return isinstance(value, self._param_type)

    def transform(self, value):
        return self._transform(value)


class StringParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type=str, error='string', **kwargs)


class IntParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type=int, error='integer', **kwargs)


    @staticmethod
    def _isinstance(value):
        try:
            a = float(value)
            b = int(a)
        except (TypeError, ValueError):
            return False
        else:
            return a == b


class FloatParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type=float, error='float', **kwargs)

    @staticmethod
    def _isinstance(value):
        try:
            float(value)
        except (TypeError, ValueError):
            return False
        else:
            return True


class BBoxParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type='bbox',
                   error='bouding box in form of Coordinates in longitude, latitude in order west, '
                         'south, east, north. CRS is epsg 4326, decimal degree', **kwargs)

    def validate(self, value):
        try:
            box(*[float(coor) for coor in value.split(',')])
            return True
        except Exception as e:
            return self._error_msg(value) + f' {e}'


class WKTParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type='wkt', error='valid WKT format', **kwargs)

    def validate(self, value):
        try:
            wkt.loads(value)
            return True
        except errors.WKTReadingError:
            return self._error_msg(value)


class DateTimeParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type='datetime', error='', **kwargs)

    def validate(self, value):
        try:
            isoparse(value)
        except ValueError:
            return self._error_msg(value)


class OptionParameter(Parameter):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, name, transform, **kwargs):
        return cls(name=name, transform=transform, param_type='multiple', error='one of', **kwargs)

    @property
    def default(self):
        return self._default

    def _error_msg(self, value):
        return f'Parameter {self._name} should be {self._error} {",".join(self.default)}. Input values is {value}'

    def validate(self, value):
        if value.find(',') == -1:
            value = [value]
        else:
            value = value.split(',')
        if all([True if val in self.default else False for val in value]):
            return True
        else:
            return self._error_msg(value)


class ServiceParameters:
    """Create dictionary containts service parameter"""

    def __init__(self, parameters):
        for setting in parameters:
            self._create_parameter(**setting)

    @classmethod
    def create(cls, parameters):
        return cls(parameters)

    def parameter(self, name):
        return getattr(self, name)

    def _create_parameter(self, name, typ, transform, **kwargs):
        setattr(self, name, typ.create(name, transform, **kwargs))

    def parameters(self):
        """return list of service parameters key names"""
        return list(self.__dict__.keys())











