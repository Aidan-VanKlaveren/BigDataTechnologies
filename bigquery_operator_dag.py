import datetime
import os
import logging
from airflow import DAG
from airflow import models
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator

today_date = datetime.datetime.now().strftime("%Y%m%d")

table_name = 'Ecommerce.total_visitors_and_views'
table_name1 = 'Ecommerce.total_visitors_and_referring_site'
table_name2 = 'Ecommerce.total_visitors_and_product_info'
yesterday = datetime.datetime.combine(
    datetime.datetime.today() - datetime.timedelta(1),
    datetime.datetime.min.time())
default_dag_args = {
    # Setting start date as yesterday starts the DAG immediately when it is
    # detected in the Cloud Storage bucket.
    'start_date': yesterday,
    # To email on failure or retry set 'email' arg to your email and enable
    # emailing here.
    'email_on_failure': False,
    'email_on_retry': False,
    # If a task fails, retry it once after waiting at least 5 minutes
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=5),
    #'project_id': models.Variable.get('gcp_project')
}

sql_query = f""" SELECT count(pageviews) as total_pageviews, count(DISTINCT fullVisitorID) as total_unique_visitors FROM `data-to-insights.ecommerce.all_sessions` """

sql_query1 = f""" SELECT channelGrouping, count(DISTINCT fullVisitorID) as total_unique_visitors FROM `data-to-insights.ecommerce.all_sessions` GROUP BY channelGrouping ORDER BY total_unique_visitors DESC """

sql_query2 = f""" SELECT v2ProductName, COUNT(pageviews) as total_pageviews, SUM(productQuantity) as total_units_ordered, SUM(productQuantity)/COUNT(productQuantity) as average_amount_per_order FROM `data-to-insights.ecommerce.all_sessions` GROUP BY v2ProductName ORDER BY total_pageviews DESC LIMIT 5 """

source = 'aidanvanklaverenassignment3:Ecommerce.total_visitors_and_product_info'

destination = 'gs://asia-east2-avkassignment3-30b2363b-bucket/data'

with DAG(dag_id='ordered_dag',
        # Continue to run DAG once per day
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')
    logging.info('trying to bq_query: ')
    logging.info('table name: ' + table_name)


    bq_query = BigQueryOperator(
        task_id='bq_query',
        sql=sql_query,
        destination_dataset_table=table_name,
        gcp_conn_id='bigquery_default',
        use_legacy_sql=False,
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        dag=dag
    )

    bq_query1 = BigQueryOperator(
        task_id='bq_query1',
        sql=sql_query1,
        destination_dataset_table=table_name1,
        gcp_conn_id='bigquery_default',
        use_legacy_sql=False,
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        dag=dag
    )

    bq_query2 = BigQueryOperator(
        task_id='bq_query2',
        sql=sql_query2,
        destination_dataset_table=table_name2,
        gcp_conn_id='bigquery_default',
        use_legacy_sql=False,
        write_disposition='WRITE_TRUNCATE',
        create_disposition='CREATE_IF_NEEDED',
        dag=dag
    )

    bq_extract = BigQueryToCloudStorageOperator(
        task_id='bq_extract',
        source_project_dataset_table=source,
        destination_cloud_storage_uris=destination,
        compression='NONE',
        export_format='CSV',
    )

    start >> bq_query >> bq_query1 >> bq_query2 >> bq_extract >> end