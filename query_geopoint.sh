#!/bin/usr/env bash

source settings.sh

curl -s -XGET $IUCN_ES_HOST/$IUCN_ES_INDEX/mammals/_search?size=100 -d '
{
   "_source": {
     "exclude": ["geometry"],
     "include": ["properties.binomial"]
    },
    "query":{
        "bool": {
            "must": {
                "match_all": {}
            },
            "filter": {
                "geo_shape": {
                    "geometry": {
                        "shape": {
                            "type": "point",
                            "coordinates" : [2.1,10.4]
                        },
                        "relation": "intersects"
                    }
                }
            }
        }
    }
}'
