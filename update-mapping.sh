echo "Creating $IUCN_ES_INDEX in $IUCN_ES_HOST"
curl -XPUT $IUCN_ES_HOST/junky -d '
{
  "mappings": {
    "paper": {
      "properties": {
        "geometry": {
          "type": "geo_shape"
        }
      }
    }
  }
}
'
