sudo apt-get update

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

