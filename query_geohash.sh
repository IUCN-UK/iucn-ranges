GET /attractions/restaurant/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "geohash_cell": {
          "location": {
            "lat":  40.718,
            "lon": -73.983
          },
          "precision": "2km" 
        }
      }
    }
  }
}
