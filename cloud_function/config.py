

class Config():
    endpoint_args_list = [
        '{"command":"quarters"}',
        '{"command":"stock_lookup", "symbol":"aapl"}',
        '{"command":"filer_lookup", "cik":"0001067983"}',
        '{"command":"stock_comparison","stockid":3598,"q1id":39,"q2id":40,"order":"q2_shares","dir":"DESC"}',
        '{"command":"holdings_comparison","filerid":163,"q1id":39,"q2id":40}',
        '{"command":"holdings","filer_ids":[349,2182],"include_13d":1}',
        '{"command":"holders","stock_ids":[195,411],"include_13d":1}'

    ]


    secret_key = 'LKuMSmJ0Y44rzP4PjKKAE3iOTnbfVaDvyO9yiseL'
    shared_key = 'AE9I6evS7Yhrc9OmxCNY'
    project_id = 'whalewisdom'
    #bigquery Config
    bg_dataset = "endpoints_data"
   
