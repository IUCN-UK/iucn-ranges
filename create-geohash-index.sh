echo "Creating $IUCN_ES_INDEX in $IUCN_ES_HOST"
curl -XPUT $IUCN_ES_HOST/$IUCN_ES_INDEX -d '
{
  "mappings": {
    "animals": {
      "properties": {
        "id_no": {
          "type": "double"
        },
        "binomial": {
          "type": "string"
        },
        "presence": {
          "type": "integer"
        },
        "origin": {
          "type": "integer"
        },
        "compiler": {
          "type": "string"
        },
        "year": {
          "type": "integer"
        },
        "citation": {
          "type": "string"
        },
        "source": {
          "type": "string"
        },
        "dist_comm": {
          "type": "string"
        },
        "island": {
          "type": "string"
        },
        "subspecies": {
          "type": "string"
        },
        "subpop": {
          "type": "string"
        },
        "data_sens": {
          "type": "string"
        },
        "sens_comm": {
          "type": "string"
        },
        "seasonal": {
          "type": "integer"
        },
        "tax_comm": {
          "type": "string"
        },
        "legend": {
          "type": "string"
        },
        "location": {
          "type": "geo_shape",
          "precision": 7
        }
      }
    }
  }
}
'
