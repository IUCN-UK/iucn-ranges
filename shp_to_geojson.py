import fiona
import json
import sys

from os import path

from shapely.geometry import mapping
from shapely.geometry import shape
from shapely.wkt import load as wkt_loads
from fiona.crs import from_epsg

import subprocess

from polyfix import fix_geometry

import sys

data = sys.argv[1]
output_file = sys.argv[2]

fixed_features = []
with fiona.open(data) as features:
    for i, feature in enumerate(features):
        print(i, feature['geometry']['type'])
        fixed_features.append(feature)

with open(output_file, 'w') as output:
    featureset = dict(type="FeatureCollection", features=fixed_features)
    output.write(json.dumps(featureset))
