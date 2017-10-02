echo "Creating $IUCN_ES_INDEX in $IUCN_ES_HOST"
curl -XPUT $IUCN_ES_HOST/$IUCN_ES_INDEX -d '
{
  "mappings": {
    "animals": {
      "properties": {
        "name": {
          "type": "string"
        },
        "location": {
          "type":               "geo_shape",
          "geohash_prefix":     true, 
          "geohash_precision":  "50km" 
        }
      }
    }
  }
}
'
