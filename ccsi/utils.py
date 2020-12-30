from pyproj import CRS

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


class ExtendedCRS(CRS):

    @classmethod
    def from_unknow(cls, crs):
        for func in [name for func in ExtendedCRS.__mro__ for name in func.__dict__.keys()
                     if name.startswith('from_') and name != 'from_unknow']:
            try:
                return getattr(ExtendedCRS, func)(crs)
            except Exception:
                pass

    @classmethod
    def from_wsf(cls, wsf):
        """
        parse wsf:srs uri i.e http://www.opengis.net/gml/srs/epsg.xml#4326. From wsf:uri is strip epsg code that is
        entered into from_epsg function. Side effect, accept also EPSG as str
        :param wsf: str - wsf:uri
        :return pyproj.CRS
        """
        loc=wsf.find('#')
        epsg = wsf[loc+1:]
        return CRS.from_epsg(epsg)

