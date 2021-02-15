from lxml import etree
from gdal import ogr, osr
from ccsi.utils import ExtendedCRS


def from_element_text(element) -> str:
    """from xtree element extract text information"""
    if element is None:
        pass
    try:
        return element.text
    except AttributeError:
        return element[0].text



def enclousure_from_text(element) -> dict:
    """function solve the problem whne link enclousure or path is in tag text"""
    try:
        return {'href': element.text}
    except AttributeError:
        return {'href': element[0].text}

def from_element_attributes(element):
    atributes = []
    if len(element) == 0:
        return [{}]
    else:
        for element in element:
            atributes.append({key: value for key, value in element.items()})
        return atributes

def from_gml_geometry(elements):
    for element in elements:
        geometry = ogr.CreateGeometryFromGML(etree.tostring(element).decode('utf-8'))
        if geometry is None:
            geometry = ogr.CreateGeometryFromGML(element.text)
            entry = etree.fromstring(element.text.encode('utf-8'))
        if geometry.IsValid():
            if geometry.GetSpatialReference() is not None:
                reference = geometry.GetSpatialReference().ExportToProj4()
                crs = ExtendedCRS.from_proj4(reference)
            else:
                crs = ExtendedCRS.from_unknow(entry.attrib.get('srsName'))
                if crs is None:
                    crs = ExtendedCRS.from_unknow(find_element('@srsName', namespace, entry)[0].get('srsName'))
                srs = osr.SpatialReference()
                srs.ImportFromEPSG(crs.to_epsg())
                geometry.AssignSpatialReference(srs)
            output = {'json': {'geometry': geometry.ExportToJson(), 'epsg': crs.to_string()},
                      'xml': {'geometry': geometry.ExportToGML(["NAMESPACE_DECL=YES"]), 'epsg': crs.to_string()}}
            geometry = None
        return output



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
    if len(elements) == 0:
        return [{}]
    else:
        for element in elements:
            atributes.append({key: value for key, value in element.items()})
        return atributes

def from_xml_attributes_del(tag, namespace, del_tags, entry):
    atributes = []
    elements = find_element(tag, namespace, entry)
    if len(elements) == 0:
        return [{}]
    else:
        for element in elements:
            if not any(element.attrib.__contains__(del_tag) for del_tag in del_tags):
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


# def from_gml_geometry(tag, namespace, entry):
#     elements = find_element(tag, namespace, entry)
#     for element in elements:
#         geometry = ogr.CreateGeometryFromGML(etree.tostring(element).decode('utf-8'))
#         if geometry is None:
#             geometry = ogr.CreateGeometryFromGML(element.text)
#             entry = etree.fromstring(element.text.encode('utf-8'))
#         if geometry.IsValid():
#             if geometry.GetSpatialReference() is not None:
#                 reference = geometry.GetSpatialReference().ExportToProj4()
#                 crs = ExtendedCRS.from_proj4(reference)
#             else:
#                 crs = ExtendedCRS.from_unknow(entry.attrib.get('srsName'))
#                 if crs is None:
#                     crs = ExtendedCRS.from_unknow(find_element('@srsName', namespace, entry)[0].get('srsName'))
#                 srs = osr.SpatialReference()
#                 srs.ImportFromEPSG(crs.to_epsg())
#                 geometry.AssignSpatialReference(srs)
#             output = {'json': {'geometry': geometry.ExportToJson(), 'epsg': crs.to_string()},
#                   'xml': {'geometry': geometry.ExportToGML(["NAMESPACE_DECL=YES"]), 'epsg': crs.to_string()}}
#             geometry = None
#         return output


def from_gdal_geometry(feature):
    geometry = feature.GetGeometryRef()
    reference = geometry.GetSpatialReference().ExportToProj4()
    crs = ExtendedCRS.from_proj4(reference)
    return {'json': {'geometry': geometry.ExportToJson(), 'epsg': crs.to_string()},
            'xml': {'geometry': geometry.ExportToGML(["NAMESPACE_DECL=YES"]), 'epsg': crs.to_string()}}


def from_xml_gml_epsg(tag, namespace, entry):
    elements = find_element(tag, namespace, entry)
    for element in elements:
        epsg = element.get(tag.strip('@'))
        if epsg is not None:
            return epsg

def pop_entry_attribute(to_pop: list, attributes:list):
    """remove unwanted entry attributes from parsed imput"""
    return {key: value for attribute in attributes for key, value in attribute.items() if key not in to_pop}
