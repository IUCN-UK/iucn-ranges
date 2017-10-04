import logging
import sys

from shapely.geometry import mapping, shape
from fiona import collection
import os

from clint.textui import progress
from clint.arguments import Args
from clint.textui import puts, colored, indent
from clint.textui.core import STDOUT, STDERR

args = Args()

shp_path = args[0]
shp_clean_path = shp_path.replace('.shp', '_clean.shp')

with indent(4):
    with collection(shp_path, "r") as input:
        schema = input.schema.copy()
        with collection(shp_clean_path, "w", "ESRI Shapefile", schema) as output:
            for f in input:
                geom = shape(f['geometry'])
                if not geom.is_valid:
                    clean = geom.buffer(0.0)
                    assert clean.geom_type == 'Polygon' or clean.geom_type == 'MultiPolygon'
                    assert clean.is_valid
                    geom = clean
                f['geometry'] = mapping(geom)
                output.write(f)
