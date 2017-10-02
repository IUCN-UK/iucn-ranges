echo $HOST
echo $INDEX
echo $POLYGONS

# create empty index
curl -XPUT '$HOST/$INDEX/'

# add polygons
ogr2ogr -progress --config ES_OVERWRITE ES_BULK=100 -f "ElasticSearch" "$HOST" "$POLYGONS" -nln $INDEX
