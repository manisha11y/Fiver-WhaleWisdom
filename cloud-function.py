import requests
from urllib.parse import quote_plus
import time
import hashlib
import hmac
import base64

# https://whalewisdom.com/shell/command[.output_type]?args=[args]&api_shared_key=[api_shared_key]&api_sig=[api_sig]
# https://whalewisdom.com/shell/command.json?api_shared_key=AE9I6evS7Yhrc9OmxCNY&api_sig=LKuMSmJ0Y44rzP4PjKKAE3iOTnbfVaDvyO9yiseL&args=%7B%22command%22:%22quarters%22%7D'


json_args = '{"command":"quarters"}'
secret_key = 'LKuMSmJ0Y44rzP4PjKKAE3iOTnbfVaDvyO9yiseL'
shared_key = 'AE9I6evS7Yhrc9OmxCNY'
formatted_args = quote_plus(json_args)
timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
digest = hashlib.sha1
raw_args=json_args+'\n'+timenow
hmac_hash = hmac.new(secret_key.encode(),raw_args.encode(),digest).digest()
sig = base64.b64encode(hmac_hash).rstrip()
url_base = 'https://whalewisdom.com/shell/command.json?'
url_args = 'args=' + formatted_args
url_end = '&api_shared_key=' + shared_key + '&api_sig=' + sig.decode() + '&timestamp=' + timenow
api_url = url_base + url_args + url_end

r = requests.get(url = api_url)
import csv   
data = r.json
# csv_file = open('downloaded.csv', 'wb')
# csv_file.write(r.content)
# csv_file.close()

import os
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= \
    '..\whalewisdom-59d534c5244d.json'

client = bigquery.Client()
job_config = bigquery.LoadJobConfig(
schema=[
    bigquery.SchemaField("Id", "STRING"),
    bigquery.SchemaField("Filling Period", "STRING"),
    bigquery.SchemaField("Status", "STRING"),
],
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,

)

load_job = client.load_table_from_json(
    r.json(),
    'WhaleWisdom.whalewisdom.quarters',
    location="US",  # Must match the destination dataset location.
    job_config=job_config,
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
print(r.json())

