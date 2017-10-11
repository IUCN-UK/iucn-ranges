from shapely.geometry import mapping
from shapely.geometry import shape
from shapely.wkt import load as wkt_loads
from os import path
import json

import subprocess

here = path.abspath(path.dirname(__file__))


def prepair_poly(shapely_poly):

    # convert to on disk featureset
    feature = dict(properties={}, geometry=mapping(shapely_poly))
    featureset = dict(type="FeatureCollection", features=[feature])

    temp_file_name = path.join(here, 'temp.geojson')
    temp_result_name = path.join(here, 'temp.wkt')

    with open(temp_file_name, 'w') as temp_file:
        temp_file.write(json.dumps(featureset))

    try:
        cmd = '/Users/bcollins/prepair/prepair --ogr {} > {}'.format(temp_file_name, temp_result_name)
        result = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 139:
            return False
        else:
            raise

    with open(temp_result_name) as t:
        part = wkt_loads(t)
    return part


def is_clockwise(vertices):
    num_vertices = len(vertices)
    area = 0
    for i in range(num_vertices):
        j = (i + 1) % num_vertices
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]
    return area < 0


def dump_to_disk(shapely_poly, feature_num, part_num):
    print('dumping feature {} part {}'.format(feature_num, part_num))
    feature = dict(properties=dict(f=feature_num, p=part_num), geometry=mapping(shapely_poly))
    featureset = dict(type="FeatureCollection", features=[feature])
    output_name = './data/feature_{}_part_{}.geojson'.format(feature_num, part_num)
    with open(output_name, 'w') as f:
        f.write(json.dumps(featureset))


def fix_polygon(shapely_poly, feature_num, part_num):
    fixed_poly = prepair_poly(shapely_poly)
    if fixed_poly is False:
        print('prepair segfault')
        dump_to_disk(shapely_poly, feature_num, part_num)
        return False
    return fixed_poly


def fix_multipolygon(geom, feature_num):
    new_coordinates = []
    for i in range(len(geom['coordinates'])):
        part_geom = geom['coordinates'][i]
        depth = len(part_geom)
        part = shape(dict(type='Polygon', coordinates=part_geom))
        if not part.is_valid:
            part = fix_polygon(part, feature_num, i)
            if part:
                new_coordinates.append(mapping(part)['coordinates'])
        else:
            new_coordinates.append(mapping(part)['coordinates'])

    geom['coordinates'] = new_coordinates
    return geom


def fix_geometry(geom, feature_num):
    shp = shape(geom)
    if not shp.is_valid:
        if geom['type'].lower() == 'multipolygon':
            return fix_multipolygon(geom, feature_num)
        if geom['type'].lower() == 'polygon':
            result = fix_polygon(shp, feature_num, 0)
            if result:
                return mapping(result)
            else:
                return result
        else:
            msg = 'Geometry type "{}" not supported'.format(geom['type'])
            raise NotImplementedError(msg)
    else:
        return geom
