with DAG('amundsen', default_args=default_args, **dag_args) as dag:

    #starting/ending dag with dummy labeling nodes is always a good practice
    start = DummyOperator(task_id="start_etl", dag=dag)
    end = DummyOperator(task_id="end_etl", dag=dag)
    
    #define schema extraction from big-query
    bigquery_extract_job = PythonOperator(
        task_id='bigquery_extract_job',
        python_callable=create_table_extract_job,
        op_kwargs={'PROJECT_ID_KEY': 'project name',
        'metadata_type': 'bigquery_metadata'} #folder name
    )

    #update last_index
    last_update_job = PythonOperator(
        task_id='last_update_job', 
        python_callable=create_last_updated_job
    )

    table_search_index_job = PythonOperator(
        task_id = 'table_search_index_job',
        python_callable = create_es_publisher_sample_job,
        op_kwargs={'elasticsearch_index_alias': 'table_search_index',
                    'elasticsearch_doc_type_key': 'table',
                    'model_name': 'databuilder.models.table_elasticsearch_document.TableESDocument',
                    'entity_type': 'table', #create tables index
                    'elasticsearch_mapping': None}
    )

    user_search_index_job = PythonOperator(
        task_id = 'user_search_index_job',
        python_callable = create_es_publisher_sample_job,
        op_kwargs={'elasticsearch_index_alias': 'user_search_index',
                    'elasticsearch_doc_type_key': 'user',
                    'model_name': 'databuilder.models.user_elasticsearch_document.UserESDocument',
                    'entity_type': 'user', #create user index
                    'elasticsearch_mapping': USER_ELASTICSEARCH_INDEX_MAPPING}
    )

    dashboard_search_index_job = PythonOperator(
        task_id = 'dashboard_search_index_job',
        python_callable = create_es_publisher_sample_job,
        op_kwargs={'elasticsearch_index_alias': 'dashboard_search_index',
                    'elasticsearch_doc_type_key': 'dashboard',
                    'model_name': 'databuilder.models.dashboard_elasticsearch_document.DashboardESDocument',
                    'entity_type': 'dashboard', #create dashboard index
                    'elasticsearch_mapping': DASHBOARD_ELASTICSEARCH_INDEX_MAPPING}
    )
    
    #define DAG path
    start >> bigquery_extract_job >> last_update_job >> table_search_index_job >> user_search_index_job >> dashboard_search_index_job >>  end
