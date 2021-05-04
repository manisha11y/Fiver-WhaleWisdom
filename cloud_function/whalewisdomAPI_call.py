import requests
from urllib.parse import quote_plus
import time
import hashlib
import hmac
import base64
from config import Config

class WhaleWisdomAPIConnect():

    def call_to_api(self, end_point_json):

        formatted_args = quote_plus(Config.json_args)
        timenow = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        digest = hashlib.sha1
        raw_args=json_args+'\n'+timenow
        hmac_hash = hmac.new(Config.secret_key.encode(),raw_args.encode(),digest).digest()
        sig = base64.b64encode(hmac_hash).rstrip()
        url_base = 'https://whalewisdom.com/shell/command.json?'
        url_args = 'args=' + formatted_args
        url_end = '&api_shared_key=' + Config.shared_key + '&api_sig=' + sig.decode() + '&timestamp=' + timenow
        api_url = url_base + url_args + url_end
        
        try:
            r = requests.get(url = api_url) 
        except:
            return 'error calling the api', 'error code'     
        

        return r.content, 'error code'

WhaleWisdomAPIConnect = WhaleWisdomAPIConnect()


