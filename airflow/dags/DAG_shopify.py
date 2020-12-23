# DAG for pulling Shopify API data and storing on S3

# Airflow imports
from __future__ import print_function
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
# General imports
from datetime import datetime, timedelta
import os

shopify_resources = ['products', 'orders']

def parseLink(link, key, pw):
    link_split = link.split(',')
    for sublink in link_split:
        split = sublink.split(';')
        if len(split) == 2 and 'next' in split[1]:
            new_link = split[0].replace('<', '').replace('>', '').strip()
            credentials = '{username}:{password}@'.format(username=key, password=pw)
            return '{}{}{}'.format(new_link[:8], credentials, new_link[8:])
    return None

def fetchDataAndSave():
    for resource in resources:
        more_results = True
        next_url = url.format(username=key, password=pw, shop=shop, api_version=api_version, resource=resource, limit=limit)
        file_count = 0
        while more_results:
            response = requests.get(next_url)
            parsed_response = json.loads(response.text)
            if resource not in parsed_response:
                print(parsed_response)
                more_results = False
            else:
                parsed_response = parsed_response[resource]
                print(resource + ' #' + str(file_count) + ': ' + str(len(parsed_response)) + ' objects')
                with open('{}-{}.json'.format(resource, str(file_count)), 'w') as outfile:
                    for row in parsed_response:
                        outfile.write(json.dumps(row))
                        outfile.write('\n')
                if 'Link' in response.headers:
                    file_count += 1
                    next_url = parseLink(response.headers['Link'], key, pw)
                    if next_url is None:
                        more_results = False
                else:
                    more_results = False
    return 0

# DAG and task info
args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['engineering@resonance.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'wait_for_downstream': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

# DAG definition
with DAG(
        dag_id='shopify',
        default_args=args,
        start_date=datetime(2019, 6, 1),
        schedule_interval='0 * * * *',
        catchup=False) as dag:

    for resource in shopify_resources:
        pull_data = PythonOperator(
            task_id='pull_{}'.format(resource),
            dag=dag,
            python_callable=fetchDataAndSave,
            op_kwargs={'resource': resource,
                       'execution_date': "{{ ds }}"})
