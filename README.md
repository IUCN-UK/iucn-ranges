##  Cleaning Geometry Approach

1. Multipart -> Single Part
2. Run each single polygon through `prepair`
3. Handle Seg. faults (fix_iucn_polygons.py)
4. Dissolve back to multipart

Note:
-----
5. Modify polyfix.py to point to your `prepair` location.

##  Elastic Search

1. Create initial index (iucn)
2. Exporting the schema to a json file (get-schema.sh)
3. Edit schema to include tree='geohash', type='geo_shape', precision='1km'
4. Delete and recreate index using schema file (update-index.sh)
5. bulk_loader to partition feature based on vertices, (Brendan uploaded the exploded version). Bulk loader will output name.part0.json files for upload loater

```bash
python bulk_loader.py ./data/iucn_exploded_clean.geojson iucn mammals
```

6. use bulk_upload.py to upload features into Elastic Search 

```bash
python bulk_upload.py $IUCN_ES_HOST iucn mammals "iucn_exploded_clean.part*.json"
```


#### Optional polysplit tool to divide polygons
https://github.com/geoloqi/polysplit
