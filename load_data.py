from os import path, environ

import json
import requests

host = environ['IUCN_ES_HOST']
index_name = environ['IUCN_ES_INDEX']
print(host)
print(index_name)

here = path.abspath(path.dirname(__file__))
data_path = path.join(here, 'data', 'iucn_polygons_wgs84.geojson')


request_template = 'POST /example/doc?refresh { "name": "Wind & Wetter, Berlin, Germany", "location": { "type": "point", "coordinates": [13.400544, 52.530286] } }'

required_fields = ['id_no',
                   'binomial',
                   'presence',
                   'origin',
                   'compiler',
                   'year',
                   'citation',
                   'source',
                   'dist_comm',
                   'island',
                   'subspecies',
                   'subpop',
                   'data_sens',
                   'sens_comm',
                   'seasonal',
                   'tax_comm',
                   'legend']

def add_record(feature):
    url = path.join(host, index_name, 'animals?refresh')
    data = feature['properties'].copy()
    fields = list(data.keys())
    for k in fields:
        if k not in required_fields:
            del data[k]

    data['location'] = feature['geometry']
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    print(resp.read())


with open(data_path, 'rb') as f:
    polys = json.loads(f.read())

for i, f in enumerate(polys['features']):
    add_record(f)
    print(i)

