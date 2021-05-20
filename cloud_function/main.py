import requests
from urllib.parse import quote_plus
from google.cloud import bigquery
import logging
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
        except Exception as e:
            logging.error('Error while calling {} endpoint : {}'.format(endpoint_name, e))
        
        if "errors" in r.text:
             return r.text, "FAILURE"
        elif r.status_code == 200:
             return r.json(), "SUCCESS"
        
    def load_to_bigquery(self, table_name, file_name, table_schema):

        client = bigquery.Client()
        dataset_ref = client.dataset(Config.bg_dataset)
        table_ref = dataset_ref.table(table_name)        
        
        try:
            job_config = bigquery.LoadJobConfig(
                schema= table_schema,
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON, 
            )
            with open(file_name, "rb") as source_file:
                    job = client.load_table_from_file(
                        source_file, table_ref, location="US", job_config=job_config)
            job.result()
        except Exception as e:
            logging.error("Error loading the records in {} table : {}".format(table_ref, e))
        else:
            logging.info("{} row(s) affected in {}".format(job.output_rows, table_name))

       
def main():
    gcp_integration = GCPIntegration()

    for json_args in Config.endpoint_args_list:

        bq_table = json.loads(json_args)["command"]
        response_file = bq_table + ".json"
        endpoint_response, status = gcp_integration.call_to_api(
                json_args, bq_table)
        try:    
            if status == "SUCCESS":      
                logging.info("Request Successful to {}".format(bq_table))
                # use '/tmp/'+response_file while deplying to cloud function :2 places
                with open(response_file, "w") as outfile:
                    for item in next(iter(endpoint_response.values())):
                        json.dump(item, outfile)
                        outfile.write('\n')
                # Choose appropriate schema for endpoints data to load data in the right way
                if bq_table == "holdings":
                    bq_schema = Config.holdings_schema
                elif bq_table == "quarters":
                    bq_schema = Config.quarters_schema
                elif  bq_table == "stock_lookup":
                    bq_table = Config.stock_lookup_schema
                elif  bq_table == "filer_lookup":
                    bq_table = Config.filer_lookup_schema
                elif  bq_table == "stock_comparison":
                    bq_table = Config.stock_comparison_schema
                elif  bq_table == "holdings_comparison":
                    bq_table = Config.holdings_comparison_schema
                elif  bq_table == "holdings":
                    bq_table = Config.holdings_schema

                gcp_integration.load_to_bigquery(bq_table, response_file, bq_schema)
            elif status == "FAILURE":
                logging.error('Error while calling {} endpoint : {}'
                        .format(bq_table, endpoint_response))
        except Exception as e:
                logging.error("Error loading the records in {} table : {}".format(bq_table, e))
        # else:
        #     logging.error('{} Error while calling {} endpoint'.format(
        #         status_code, bq_table))


logging.basicConfig(level=logging.DEBUG)

gcp_integration=GCPIntegration()
# gcp_integration.main()
# gcp_integration.load_to_bigquery("holdings", "holdings.json")
main()
# gcp_integration.load_to_bigquery("holdings", "holdings.json")

