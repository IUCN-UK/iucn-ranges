import fiona
import json
import sys

from os import path

from toolz.itertoolz import partition_all

from shapely.geometry import mapping
from shapely.geometry import shape
from shapely.wkt import load as wkt_loads

import subprocess

from polyfix import fix_geometry


def count_vertices(geometry):
    geom_type = geometry['type'].lower()
    if geom_type == 'polygon':
        return len(geometry['coordinates'])
    elif geom_type == 'multipolygon':
        return sum([len(poly) for poly in geometry['coordinates']])
    else:
        raise NotImplementedError('Geometry type "{}" is not supported'.format(geom_type))


def vpartition_features(shp_path, index_name, type_name, output_prefix=None, max_size=10000):

    if not output_prefix:
        file_name = path.split(shp_path)[1]
        file_split, _ = path.splitext(file_name)
        output_prefix = file_split + '.part'

    counter = 0
    batch = []
    batch_size = 0
    batch_num = 0

    with fiona.open(shp_path) as features:
        for feature in features:
            if not feature['geometry']:
                continue

            batch.append(feature)
            batch_size += count_vertices(feature['geometry'])

            if batch_size > max_size:
                output_file = '{}{}.json'.format(output_prefix, batch_num)
                batch_num += 1
                print(output_file)
                with open(output_file, 'w') as out:
                    for j, f in enumerate(batch):
                        counter = counter + 1
                        i_line = dict(_index=index_name,
                                      _type=type_name,
                                      _id=str(counter))
                        out.write(json.dumps(dict(create=i_line)) + '\n')
                        out.write(json.dumps(f) + '\n')
                    batch = []
                    batch_size = 0

if __name__ == '__main__':
    shp_path = sys.argv[1]
    index_name = sys.argv[2]
    type_name = sys.argv[3]

    vpartition_features(shp_path, index_name, type_name)
