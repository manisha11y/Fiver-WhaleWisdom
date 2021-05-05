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

    def call_to_api(self, json_args, endpoint_name):

        formatted_args = quote_plus(json_args)
        timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        digest = hashlib.sha1
        raw_args = json_args+'\n'+timenow
        hmac_hash = hmac.new(Config.secret_key.encode(),
                             raw_args.encode(), digest).digest()
        sig = base64.b64encode(hmac_hash).rstrip()
        url_base = 'https://whalewisdom.com/shell/command.json?'
        url_args = 'args=' + formatted_args
        url_end = '&api_shared_key=' + Config.shared_key + \
            '&api_sig=' + sig.decode() + '&timestamp=' + timenow
        api_url = url_base + url_args + url_end
 
        try:
            r = requests.get(url=api_url)
            print("Request Successful to {}".format(endpoint_name))
        except:
            print('Error while calling {} endpoint'.format(endpoint_name))

        return r.json(), r.status_code

    def load_to_bigquery(self, table_name, file_name):
        client = bigquery.Client()
        
        dataset_ref = client.dataset(Config.bg_dataset)
        table_ref = dataset_ref.table(table_name)
        print(table_ref)
        job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, autodetect=True,
        )

        with open(file_name, "rb") as source_file:
            job = client.load_table_from_file(
                source_file,table_ref , location="US", job_config=job_config)

        job.result()
        table = client.get_table(table_name)  # Make an API request.
        print(
            "Loaded {} rows and {} columns to {}".format(
                table.num_rows, len(table.schema), table_name
            )
        )            

    def main(self, context=None):
        gcp_integration=GCPIntegration()

        for json_args in Config.endpoint_args_list:
            
            bq_table=json.loads(json_args)["command"]
            response_file=bq_table + ".json"

            response_json, status_code=gcp_integration.call_to_api(
                json_args, bq_table)
            
            
            if status_code == 200:
                with open(response_file, "w") as outfile:
                    for item in next(iter(response_json.values())):
                        json.dump(item, outfile)
                        outfile.write('\n')
                try:
                    gcp_integration.load_to_bigquery(bq_table, response_file)
                except ValueError as e:
                    print("Error loading the records in {} table : {}".format(bq_table, e))
            else:
                print('{} Error while calling {} endpoint'.format(
                    status_code, bq_table))


gcp_integration=GCPIntegration()
gcp_integration.main()
