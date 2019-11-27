sudo apt-get update

# ==========================================================
# Install ElasticSearch with Debian. Prerequisites Java 8/11
# https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html

# Download and install the public signing key:
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Install the apt-transport-https:
sudo apt-get install apt-transport-https

# Save the repository definition to /etc/apt/sources.list.d/elastic-7.x.list:
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

# Install the ElasticSearch
sudo apt-get update && sudo apt-get install elasticsearch

# Start ElasticSearch
sudo systemctl start elasticsearch.service

# Test ElasticSearch, open http://localhost:9200
curl -X GET 'http://localhost:9200'

# Stop ElasticSearch
# sudo systemctl stop elasticsearch.service

# Install python3 package. Prerequisites python3 pip
python3 -m pip install elasticsearch

# ==========================================================
# Install Kibana with Debian
# https://www.elastic.co/guide/en/kibana/current/deb.html

# Download and install the public signing key:
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

# Install the apt-transport-https:
sudo apt-get install apt-transport-https

# Save the repository definition to /etc/apt/sources.list.d/elastic-7.x.list:
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

# Install the Kibana
sudo apt-get update && sudo apt-get install kibana

# Start Kibana
sudo systemctl start kibana.service

# Test Kibana, open http://localhost:5601

# Stop Kibana
# sudo systemctl stop kibana.service

# ==========================================================
# Install Apache Solr 8.3. Prerequisites Java 8+
# https://tecadmin.net/install-apache-solr-on-debian/

# Install java:
# sudo apt install default-java

# Test java:
# java -version

# Download Solr:
wget http://www-eu.apache.org/dist/lucene/solr/8.3.0/solr-8.3.0.tgz

# Install Solr to home:
tar xzf solr-8.3.0.tgz solr-8.3.0/bin/install_solr_service.sh --strip-components=2
sudo bash ./install_solr_service.sh solr-8.3.0.tgz -i ~/

# Start Solr
# sudo systemctl start solr

# Start Solr in SolrCloud Mode
~/solr/bin/solr start -e cloud
# or
# ~/solr/bin/solr start -cloud -p 7574 -s ~/solr/bin/example/cloud/node1/solr

# Test Solr, http://localhost:7574/solr/

# Stop Solr
# ~/solr/bin/solr stop -all

# Clear Solr
# rm -Rf ~/solr/example/cloud/

# Install python3 package. Prerequisites python3 pip
python3 -m pip install pysolr

