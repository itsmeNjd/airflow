from elasticsearch import Elasticsearch

from airflow import DAG 
from airflow import macros  
from airflow.operators.python_operator import PythonOperator 
from airflow.operators.dummy_operator import DummyOperator
from pyhocon import ConfigFactory

from databuilder.publisher.elasticsearch_constants import DASHBOARD_ELASTICSEARCH_INDEX_MAPPING, USER_ELASTICSEARCH_INDEX_MAPPING
from databuilder.extractor.bigquery_metadata_extractor import BigQueryMetadataExtractor
from databuilder.publisher.elasticsearch_publisher import ElasticsearchPublisher
from databuilder.extractor.neo4j_extractor import Neo4jExtractor
from databuilder.job.job import DefaultJob
from databuilder.extractor.neo4j_es_last_updated_extractor import Neo4jEsLastUpdatedExtractor
from databuilder.extractor.neo4j_search_data_extractor import Neo4jSearchDataExtractor
from databuilder.loader.file_system_elasticsearch_json_loader import FSElasticsearchJSONLoader
from databuilder.loader.file_system_neo4j_csv_loader import FsNeo4jCSVLoader
from databuilder.publisher import neo4j_csv_publisher
from databuilder.publisher.neo4j_csv_publisher import Neo4jCsvPublisher
from databuilder.task.task import DefaultTask
from databuilder.transformer.base_transformer import NoopTransformer


dag_args = {
    'concurrency': 10,
    # One dagrun at a time
    'max_active_runs': 1,
    # 1AM, 1PM EET
    'schedule_interval': '0 11 * * *',
    'catchup': False
}

default_args = {
    'owner': 'Salma Amr',
    'start_date': datetime(2020, 9, 16),
    'depends_on_past': False,
    'email': ['salma.abdelfattah@talabat.com'],
    'email_on_failure': True,
    'bigquery_conn_id': 'bigquery_default'
}

es_host = 'gcp machine ip'
es_port = os.getenv('CREDENTIALS_ELASTICSEARCH_PROXY_PORT', 9200) #amundsen default es port, override env variable with target ip

neo_host = 'gcp machine ip'
neo_port = os.getenv('CREDENTIALS_NEO4J_PROXY_PORT', 7687) #amundsen default neo4j db server port, override env variable with target ip

es = Elasticsearch([
    {'host': es_host, 'port': es_port},
])

NEO4J_ENDPOINT = 'bolt://{}:{}'.format(neo_host, neo_port) #neo4j graphical interface uses bolt protocol
#default docker image sets uname and password as below
neo4j_user = 'neo4j' 
neo4j_password = 'test'
