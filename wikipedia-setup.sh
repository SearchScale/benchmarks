curl "http://${SOLRHOST}/solr/admin/collections?action=CREATE&name=wikipedia&numShards=3"

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"abstract",
     "type":"text_general",
     "stored":true, "multiValued":false }
}' http://${SOLRHOST}/solr/wikipedia/schema

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field":{
     "name":"topic",
     "type":"text_general",
     "stored":true, "multiValued":false }
}' http://${SOLRHOST}/solr/wikipedia/schema


