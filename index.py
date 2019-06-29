#!/usr/bin/env python3

import sys, json;
import solr
import time
import requests
import os

#sys.stdin.reconfigure(encoding='ISO-8859-1')
os.environ['PYTHONIOENCODING'] = 'ISO-8859-1'
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("/tmp/wiki_batch_logfile.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)  
        self.log.flush()
    def flush(self):
        pass

sys.stdout = Logger()

# XXX main function to add documents in a batch to solr
def send_to_solr(s, articles, synerr):
	try:
		s.add_many(articles, commit=False)
	except:
		print("Caught error in Unicode")
		synerr+= 1


solrUrl = "35.232.98.133:30983"
batchSize = 100000

# XXX Connect to solr first, we must crash if it is not around...
s = solr.Solr('http://' + solrUrl + '/solr/wikipedia')


# XXX first ensure the collection is empty
headers = {'Content-Type': 'application/xml'} 
resp = requests.post(url = 'http://' + solrUrl + '/solr/wikipedia/update', data =
'<delete><query>*:*</query></delete>', headers = headers)
if resp.status_code != 200:
	print("Could not flush collection")
	sys.exit(0)
print("sent delete all...")
resp = requests.post(url = 'http://' + solrUrl + '/solr/wikipedia/update', data = '<commit/>', headers = headers)
if resp.status_code != 200:
	print("Could not flush collection")
	print(resp)
	sys.exit(0)
print("Deleted all...")

# Counter to batch input to solr
cnt=0
synerr=0
articles = []
start = time.time()
numiter = 0
docid = 1
for line in sys.stdin:
	cnt+=1
	docid += 1

	# Do TSV parsing...
	fields = line.split('\t')
	topic = fields[0]
	date = fields[1]
	abst = fields[2]
	articles.append({'id': docid, 'topic': topic, 'date' : date, 'abstract': abst})
	if cnt >= batchSize:
		send_to_solr(s, articles, synerr)
		cnt = 0
		print("Adding... " + str(numiter))
		numiter += 1
		articles = []
# Catch last iteration
print("count of last push is " + str(cnt))
print(" Total documents pushed = " + str(numiter * batchSize + cnt))
s.add_many(articles, commit=True)
end = time.time()

print("Total error lines count is " + str(synerr))

# XXX Now for the benchmark
resp = requests.get('http://' + solrUrl + '/solr/wikipedia/select?q=*:*')
if resp.status_code != 200:
	print("some issue")
output = resp.json()
totdocs = output['response']['numFound']

tottime = end - start # In seconds
docspersec = int(totdocs/tottime)
print("Total documents is " + str(totdocs) + "& time taken is " + str(tottime))
print("The total throughput we got it " + str(docspersec) + " docs per second")
