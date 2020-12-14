from lxml import etree
from gdal import ogr, osr


def find_element(tag, namespace, entry):
    prefix = namespace.get('prefix')
    ns = namespace.get('namespace')
    if tag.startswith('@'):
        try:
            return entry.findall(f'.//{prefix}:*[{tag}]', namespaces={prefix: ns})
        except SyntaxError:
            return entry.findall(f'.//{prefix}*[{tag}]', namespaces={prefix: ns})
    else:
        try:
            return entry.findall(f'.//{prefix}:{tag}', namespaces={prefix: ns})
        except (SyntaxError, KeyError):
            return entry.findall(f'.//{prefix}{tag}', namespaces={prefix: ns})


def from_xml_attributes(tag, namespace, entry):
    atributes = []
    elements = find_element(tag, namespace, entry)
    for element in elements:
        atributes.append({key: value for key, value in element.items()})
    return atributes


def from_xml_text(tag, namespace, entry):
    elements = find_element(tag, namespace, entry)
    text = [element.text for element in elements]
    if isinstance(text, list):
        if len(text) == 0:
            return None
        return text[0]
    return text


def from_xml_gml_geometry(tag, namespace, entry):
    elements = find_element(tag, namespace, entry)
    for element in elements:
        geometry = ogr.CreateGeometryFromGML(etree.tostring(element).decode('utf-8'))
        if geometry is not None and geometry.IsValid():
            if geometry.GetSpatialReference() is None:
                epsg = int(find_element('@srsName', namespace, entry)[0].get('srsName').strip('EPSG:'))
                srs = osr.SpatialReference()
                srs.ImportFromEPSG(epsg)
                geometry.AssignSpatialReference(srs)
                return {'geometry': geometry, 'epsg': epsg}


def from_xml_gml_epsg(tag, namespace, entry):
    elements = find_element(tag, namespace, entry)
    for element in elements:
        epsg = element.get(tag.strip('@'))
        if epsg is not None:
            return epsg







