def create_last_updated_job():

    # loader saves data to these folders and publisher reads it from here
    tmp_folder = '/var/tmp/amundsen/last_updated_data'
    node_files_folder = '{tmp_folder}/nodes'.format(tmp_folder=tmp_folder)
    relationship_files_folder = '{tmp_folder}/relationships'.format(tmp_folder=tmp_folder)

    task = DefaultTask(extractor=Neo4jEsLastUpdatedExtractor(),
                       loader=FsNeo4jCSVLoader())

    job_config = ConfigFactory.from_dict({
        'extractor.neo4j_es_last_updated.model_class':
            'databuilder.models.neo4j_es_last_updated.Neo4jESLastUpdated',
        'loader.filesystem_csv_neo4j.node_dir_path': node_files_folder,
        'loader.filesystem_csv_neo4j.relationship_dir_path': relationship_files_folder,
        'publisher.neo4j.node_files_directory': node_files_folder,
        'publisher.neo4j.relation_files_directory': relationship_files_folder,
        'publisher.neo4j.neo4j_endpoint': NEO4J_ENDPOINT,
        'publisher.neo4j.neo4j_user': neo4j_user,
        'publisher.neo4j.neo4j_password': neo4j_password,
        'publisher.neo4j.neo4j_encrypted': False,
        'publisher.neo4j.job_publish_tag': 'unique_lastupdated_tag',  # should use unique tag here like {ds}
    })

    job = DefaultJob(conf=job_config,
                    task=task,
                    publisher=Neo4jCsvPublisher())
    job.launch()
