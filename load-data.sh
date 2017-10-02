export IUCN_ES_HOST = "https://search-icuntest-w752w6xxvrbcfrzb3lnmbgr24e.us-east-1.es.amazonaws.com"
export IUCN_ES_INDEX = "myindex"
export ICUN_ES_POLYGONS = "./data/iucn_polygons_wgs84.geojson"
export WEB_TUTORIAL = "https://mapbutcher.gitbooks.io/using-spatial-data-in-elasticsearch/content/exercise_2_-_indexing_some_spatial_data/create_index.html"

echo $HOST
echo $INDEX
echo $POLYGONS

# create empty index
curl -XPUT '$HOST/$INDEX/'

# add polygons
ogr2ogr -progress --config ES_OVERWRITE ES_BULK=100 -f "ElasticSearch" "$HOST" "$POLYGONS" -nln $INDEX
