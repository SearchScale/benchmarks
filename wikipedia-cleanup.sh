curl "http://${SOLRHOST}/solr/admin/collections?action=DELETE&name=wikipedia"
curl "http://${SOLRHOST}/solr/admin/configs?action=DELETE&name=wikipedia.AUTOCREATED"
