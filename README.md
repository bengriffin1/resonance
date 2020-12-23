___Resonance HW Steps___
1. **create script to pull API data
2. **upload to s3 bucket
3. **run crawlers
4. **explore in athena
5. **hook up mode analytics
6. **start up airflow cluster
7. **load / run dags
8. transformations
9. ci/cd
10. looker, snowflake
11. developer workflow


___AWS Airflow Setup___
Use the mwaa-vpc-cfn.yaml cloudformation template to create a VPC for airflow
Create a S3 bucket for the Airflow code, then create a MWAA cluster pointing to the bucket
Upload DAG code to the S3 bucket
Use the UI to open Airflow and trigger your DAG

___Glue Crawler Setup___
Use Glue to create a new user that is allowed to crawl your data. Most issues with crawlers are S3 permission issues.
Create a new crawler for each "table" or different data structure, and point it to S3 and start it.

___Mode Analytics Setup___
Log into mode.com and set up an account
Create an S3 bucket for Athena results
Create a user in AWS that has READ access to your S3 bucket (both for data and Athena results), and READ access to your Glue catalog. This is a programmatic only user.
Enter the credentials + s3 bucket into Mode under a new connection

___Local Airflow Startup___
Create a virtualenv, activate it and install requirements.txt (pip install -r requirements.txt)
Run the below to set up airflow:

`export AIRFLOW_HOME=~/airflow
airflow db init
airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@resonance.nyc
airflow webserver --port 8080
airflow scheduler # run in separate window from webserver
airflow test DAGNAME TASKNAME DATE # Run this to test a single task`


___Shopify Object Notes___
products
  should we include collections?
orders (only last 60 days?, need to request access for more)
  refunds, included in orders but can be standalone
  checkouts (abandoned checkouts)
analytics (not including, only aggregations)
customers (not including)


___Things to consider___
security, PII
maybe set up reports for each store in Shopify until we get a UI
cadence of retrieving data... airflow?
  every hour, pull data from last timestamp?
compression of jsons in s3
issues w athena? > complex queries and slow runtime
next steps, deduping/ most recent view, splitting into real tables, applying transformations
I wouldn't use glue crawlers, just hand-write schemas
hook up alerting to airflow
kafka + webhooks, possibly stream directly into snowflake?
Using docker containers for developer workflow


___Tradeoff Notes___

BI Tool:
               user knowledge | development speed
Looker             low                  low
Mode               high                 high


Database:
             query complexity | cost | development speed | query speed | etl complexity
athena json     high            low         high             low             low
snowflake       low             high        low              high            high
athena parquet  low             med         low              med             high
