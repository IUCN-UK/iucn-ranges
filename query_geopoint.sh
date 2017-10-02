#!/bin/usr/env bash

# Empty field variables
LON=''
LAT=''
LABEL=''

while [[ $# -gt 0 ]]
do
  case $1 in
    --label)
      LABEL=$2
      shift;;
    --lon)
      LON=$2
      shift;;
    --lat)
      LAT=$2
      shift;;
    --radius)
      RADIUS=$2
      shift;;
    --)
      shift
      break;;
    --*)
      echo "$0: error - unrecognized option $1" 1>&2
      help;exit 1;;
    -?)
      echo "$0: error - unrecognized option $1" 1>&2
      help;exit 1;;
    *)
      break;;
    esac
    shift
done

# Sanity-check:
: ${LON:?'Oops! LON is not defined!?'}
: ${LAT:?'Oops! LAT is not defined!?'}

inline_shape $LON $LAT

source settings.sh
curl -XGET $IUCN_ES_HOST/$IUCN_ES_INDEX -d '_search
{
    "query":{
        "bool": {
            "must": {
                "match_all": {}
            },
            "filter": {
                "geo_shape": {
                    "location": {
                        "shape": {
                            "type": "point",
                            "coordinates" : [LON,LAT]
                        },
                        "relation": "within"
                    }
                }
            }
        }
    }
}
'
