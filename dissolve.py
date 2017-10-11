import fiona
import json
import sys

from os import path

from shapely.geometry import mapping
from shapely.geometry import shape
from shapely.wkt import load as wkt_loads
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
import fiona
import itertools

data = sys.argv[1]
output_file = sys.argv[2]
field = sys.argv[3]

features = []
with fiona.open(data) as input_file:
    e = sorted(input_file, key=lambda k: k['properties'][field])
    for key, group in itertools.groupby(e, key=lambda x:x['properties'][field]):
        geoms = []
        props = None
        for feature in group:
            if feature['geometry']:
                shp = shape(feature['geometry'])
                geoms.append(shp)
                props = feature['properties']
        feature = {'geometry': mapping(unary_union(geoms)), 'properties': props}
        features.append(feature)

with open(output_file, 'w') as output:
    featureset = dict(type="FeatureCollection", features=features)
    output.write(json.dumps(featureset))
