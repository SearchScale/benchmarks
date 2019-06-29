# benchmarks

    ./wikipedia-download.sh
    sudo apt install python3-pip
    sudo pip3 install solrpy
    
    export SOLRHOST="localhost:8983"
    
    #adjust the batch size and solr url in index.py
    vi index.py
    
    ./wikipedia-setup.sh
    
    xzcat enwiki-20120502-lines-1k.txt.lzma | python3 index.py
    
    #once down or before every new indexing run,
    ./wikipedia-cleanup.sh
