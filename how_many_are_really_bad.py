import fiona
from shapely.geometry import shape
import sys
import json

shp_path = sys.argv[1]

with fiona.open(shp_path) as featureset:
    for i, feature in enumerate(featureset):
        geom = shape(feature['geometry'])
        if not geom.is_valid:
            geom = geom.buffer(0)
            if not geom.is_valid:
                print(i)
