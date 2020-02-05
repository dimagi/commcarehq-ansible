title: ES upgrade from 1.7.6 to 2.4.6
key: Es-upgrade
date: 2020-02-05
optional_per_env: yes
upgrading_steps: |

  1. stop the site

  commcare-cloud <env> downtime start
  
  2. Change the es version and checksum in commcare-cloud/environments/<env>/public.yml 
  
  elasticsearch_version: 2.4.6
  elasticsearch_download_sha256: 5f7e4bb792917bb7ffc2a5f612dfec87416d54563f795d6a70637befef4cfc6f.
  ELASTICSEARCH_MAJOR_VERSION=2

  3. update the local settings
  
  commcare-cloud <env> update-config

  4.login to any ES server and disable the cluster routing
  
  curl -XPUT Elasticsearchserver-IP:9200/_cluster/settings -d '{\"transient\" : {\"cluster.routing.allocation.enable\" : \"none\" }}'

  5. stop the monit and Elasticsearch service
  
  cchq <env> run-shell-command all "service monit stop" -b --limit=elasticsearch
  cchq <env> run-shell-command all "service elasticsearch stop" -b --limit=elasticsearch

  6.download and extract the new version with below command and which will start the ES service with new version also
   
  commcare-cloud <env> ansible-playbook deploy_stack.yml --limit=elasticsearch --tags=elasticsearch

  7.stop the monit and Elasticsearch service
 
  cchq <env> run-shell-command all "service monit stop" -b --limit=elasticsearch
  cchq <env> run-shell-command all "service elasticsearch stop" -b --limit=elasticsearch

  8. rename the 1.7.6 ES data folder with new version 2.4.6
  
  cchq <env> run-shell-command all "mv /opt/data/elasticsearch-2.4.6 /opt/data/elasticsearch-2.4.6-new-installation" -b --limit=elasticsearch
  cchq <env> run-shell-command all "mv /opt/data/elasticsearch-1.7.6 /opt/data/elasticsearch-2.4.6" -b --limit=elasticsearch

  9.verify the permissions of data folder and new data direcory size
 
  cchq <env> run-shell-command all "du -ch /opt/data/elasticsearch-2.4.6" -b --limit=elasticsearch

  10. start the monit and Elasticsearch sevice
 
  cchq <env> run-shell-command all "service monit start" -b --limit=elasticsearch
  cchq <env> run-shell-command all "service elasticsearch start" -b --limit=elasticsearch

  11. verify the cluster status and if it is yello state then enable the cluster routing and start the site

  cchq <env> run-shell-command all "curl -XGET '<ES-IP>:9200/_cluster/health?pretty'" -b --limit=elasticsearch

  12. Login to anyserver and enable the cluster routing
  
  curl -XPUT Elasticsearchserver-IP:9200/_cluster/settings -d '{\"transient\" : {\"cluster.routing.allocation.enable\" : \"all\" }}'

  13.start the site
  
  commcare-cloud <env> downtime end