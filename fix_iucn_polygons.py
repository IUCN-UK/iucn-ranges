import json
import sys
from os import path
from glob import glob
import subprocess
import sys
from collections import defaultdict

from shapely.geometry import mapping
from shapely.geometry import shape
from shapely.wkt import load as wkt_loads
from fiona.crs import from_epsg

import fiona

from polyfix import fix_geometry



def glob_features(expression):

    for p in glob(expression):
        with fiona.open(p) as features:
            for f in features:
                yield f


def fix(input_data, output_file_path):
    out_features = []
    for i, feature in enumerate(glob_features(input_data)):
        fixed_geometry = fix_geometry(feature['geometry'], i)
        if fix_geometry:
            feature['geometry'] = fix_geometry(feature['geometry'], i)
            out_features.append(feature)
        else:
            print('DROPPING {}'.format(i))

    with open(output_file, 'w') as output:
        featureset = dict(type="FeatureCollection", features=fixed_features)
        output.write(json.dumps(featureset))


if __name__ == '__main__':
    input_data = sys.argv[1]
    output_file_path = sys.argv[2]
    fix(input_data, output_file_path)
    
