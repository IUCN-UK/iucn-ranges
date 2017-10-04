import sys
import fiona
import json

shp_path = sys.argv[1]
index_name = sys.argv[2]
type_name = sys.argv[3]
output_file = sys.argv[4]

with fiona.open(shp_path) as features:
    with open(output_file, 'w') as out:
        for i, f in enumerate(features):
            if i > 100:
                break
            i_line = dict(_index=index_name,
                           _type=type_name,
                           _id=str(i))
            out.write(json.dumps(dict(create=i_line))+ '\n')
            out.write(json.dumps(f) + '\n')
