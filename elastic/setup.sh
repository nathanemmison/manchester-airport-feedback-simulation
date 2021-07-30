docker stop kib01-test
docker stop es01-test

docker rm es01-test
docker rm kib01-test

docker network rm elastic

docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.13.4
docker run --name es01-test --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -d docker.elastic.co/elasticsearch/elasticsearch:7.13.4

docker pull docker.elastic.co/kibana/kibana:7.13.4
docker run --name kib01-test --net elastic -p 5601:5601 -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" -d docker.elastic.co/kibana/kibana:7.13.4

sleep 20

curl -X PUT "localhost:9200/_template/toilets?pretty" -H 'Content-Type: application/json' -d'
{
  "index_patterns": ["toilets", "toilets*", "*toilets"],
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "toilet_id": {
        "type": "keyword"
      },
      "name": {
        "type": "keyword"
      },
      "rating": {
        "type": "integer"
      },
      "timestamp": {
        "type": "date",
        "format": "epoch_second"
      },
      "location": {
        "type": "geo_point"
      }
    }
  }
}
'

python feedback.py