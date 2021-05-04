import requests
from urllib.parse import quote_plus
from google.cloud import bigquery
import time
import hashlib
import hmac
import base64
from config import Config
import json
import csv

class GCPIntegration():
    json_args_list = ['{"command":"quarters"}'
    #  '{"command":"holdings_comparison","filerid":163,"q1id":39,"q2id":40}'
]
    secret_key = 'LKuMSmJ0Y44rzP4PjKKAE3iOTnbfVaDvyO9yiseL'
    shared_key = 'AE9I6evS7Yhrc9O'

    def call_to_api(self, json_args):

        formatted_args = quote_plus(Config.json_args)
        timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        digest = hashlib.sha1
        raw_args=json_args+'\n'+timenow
        hmac_hash = hmac.new(Config.secret_key.encode(),raw_args.encode(),digest).digest()
        sig = base64.b64encode(hmac_hash).rstrip()
        url_base = 'https://whalewisdom.com/shell/command.csv?'
        url_args = 'args=' + formatted_args
        url_end = '&api_shared_key=' + Config.shared_key + '&api_sig=' + sig.decode() + '&timestamp=' + timenow
        api_url = url_base + url_args + url_end
        
        try:
            r = requests.get(url = api_url) 
        except:
            return 'error calling the api', r.status_code 
        
        return r.content, r.status_code


    def load_to_bigquery(self):
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= \
            '..\whalewisdom-59d534c5244d.json'

        client = bigquery.Client()
        job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("Id", "STRING"),
            bigquery.SchemaField("Filling Period", "STRING"),
            bigquery.SchemaField("Status", "STRING"),
        ],
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV,
        )

        load_job = client.load_table_from_json(
            "downloaded.csv",
            'WhaleWisdom.whalewisdom.quarters',
            location="US",  # Must match the destination dataset location.
            job_config=job_config,
        )  # Make an API request.

        load_job.result()  # Waits for the job to complete.

        destination_table = client.get_table(table_id)
        print("Loaded {} rows.".format(destination_table.num_rows))
        

    def main(event, context=None):
        gcp_integration = GCPIntegration()
        for json_args in gcp_integration.json_args_list:
            response_csv, status_code = gcp_integration.call_to_api(json_args)
            csv_file = open('downloaded.csv', 'wb')
            csv_file. write(response_csv)
            # csv_file. close()
            print('created response csv')


            # with open("sample.json", "w") as outfile: 
            #     json.dump(response_json, outfile)
            gcp_integration.load_to_bigquery()

        
        # print(response_json)
        print(status_code)

gcp_integration = GCPIntegration()
gcp_integration.main()
# gcp_integration.load_to_bigquery()

