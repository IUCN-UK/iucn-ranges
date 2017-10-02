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
    --lon_min)
      LON_MIN=$2
      shift;;
    --lon_max)
      LON_MAX=$2
      shift;;
    --lat_min)
      LAT_MIN=$2
      shift;;
    --lat_max)
      LAT_MAX=$2
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
: ${LON_MIN:?'Oops! LON_MIN is not defined!?'}
: ${LAT_MIN:?'Oops! LAT_MIN is not defined!?'}
: ${LON_MAX:?'Oops! LON_MAX is not defined!?'}
: ${LAT_MAX:?'Oops! LAT_MAX is not defined!?'}

source settings.sh
curl -H "Content-Type: application/json" -X GET $IUCN_ES_HOST/$IUCN_ES_INDEX -d '_search
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
                            "type": "envelope",
                            "coordinates" : [[LON_MIN,LAT_MIN],[LON_MAX,LAT_MAX]]
                        },
                        "relation": "within"
                    }
                }
            }
        }
    }
}
'
