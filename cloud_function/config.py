import google.cloud.bigquery as bigquery


class Config():

    secret_key = 'LKuMSmJ0Y44rzP4PjKKAE3iOTnbfVaDvyO9yiseL'
    shared_key = 'AE9I6evS7Yhrc9OmxCNY'
    project_id = 'whalewisdom'

    endpoint_args_list = [
        '{"command":"quarters"}',
        '{"command":"stock_lookup", "name":"Apple Comp"}',
        '{"command":"filer_lookup", "name":"berkshire"}',
        '{"command":"stock_comparison","stockid":3598,"q1id":39,"q2id":40,"order":"q2_shares","dir":"DESC"}',
        '{"command":"holdings_comparison","filerid":163,"q1id":39,"q2id":40}',
        # '{"command":"holdings","filer_ids":[289989,2911,297583,279570,328606,70329,48797,2715,1238,102758],"all_quarters":1}'
        # '{"command":"holdings","filer_ids":[152,163719,1249,22,96740,289090,358445,319105,328336,328353],"all_quarters":1}'
        # '{"command":"holdings","filer_ids":[336386,327443,166331,1226,1163,328436,261,358382,264203,895],"all_quarters":1}'
        # '{"command":"holdings","filer_ids":[75916,221641,66684,143033,287250,1833,200259,256630,289089,287818],"all_quarters":1}'
        # '{"command":"holdings","filer_ids":[366313,358409,288840,334872,135224,2514,178001,106401,208467,358129],"all_quarters":1}'
        # '{"command":"holdings","filer_ids":[2395,327965,297371,2358,200181,288864,66809,358608,288798,211631],"all_quarters":1}'
        # '{"command":"holdings","filer_ids":[93698,256486,122,327881,298386,289052,249588,215421,197090,339162],"all_quarters":1}'
        '{"command":"holders","stock_ids":[195,411]}'

    ]

    # bigquery Config
    bg_dataset = "endpoints_data"

    # Holdings Schema
    holdings_schema = [
        bigquery.SchemaField("filer_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("filer_id", "INTEGER", mode="NULLABLE"),

        bigquery.SchemaField(
            "records",
            "RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField("quarter_id",	"INTEGER",	mode="NULLABLE"),
                bigquery.SchemaField("quarter",	"DATE",	mode="NULLABLE"),
                bigquery.SchemaField(
                    "date_last_filed",	"DATE",	mode="NULLABLE"),
                bigquery.SchemaField(
                    "holdings",
                    "RECORD",
                    mode="REPEATED",
                fields=[
                     bigquery.SchemaField(
                            "quarter_id_owned","INTEGER", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "percent_change","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "avg_price","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "filer_state","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "source_date","DATE", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "stock_id","INTEGER", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "previous_shares","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "current_shares","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "shares_change","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "source","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "previous_mv","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "current_percent_of_portfolio","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "previous_percent_of_portfolio","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "current_mv","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "previous_ranking","INTEGER", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "filer_city","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "filer_street_address","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "percent_ownership","FLOAT", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "filer_zip_code","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "sector","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "current_ranking","INTEGER", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "industry","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "position_change_type","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "security_type","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "stock_ticker","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "filer_id","INTEGER", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "stock_name","STRING", mode="NULLABLE"),
                     bigquery.SchemaField(
                            "filer_name","STRING", mode="NULLABLE"),
                    ],
                ),
            ],
        ),
    ]

    quarters_schema = [
        bigquery.SchemaField("status",	"STRING",	mode="NULLABLE"),
        bigquery.SchemaField("filing_period",	"DATE",	mode="NULLABLE"),
        bigquery.SchemaField("id",	"INTEGER",	mode="NULLABLE")

    ]

    stock_lookup_schema = [
        bigquery.SchemaField("status",	"STRING",	mode="NULLABLE"),
        bigquery.SchemaField("name",	"STRING",	mode="NULLABLE"),
        bigquery.SchemaField("link",	"STRING",	mode="NULLABLE"),
        bigquery.SchemaField("cusip",	"STRING",	mode="NULLABLE"),
        bigquery.SchemaField("ticker",	"STRING",	mode="NULLABLE"),
        bigquery.SchemaField("id",	"INTEGER",	mode="NULLABLE")
    ]

    filer_lookup_schema = [
        bigquery.SchemaField("state_incorporation",	"STRING", mode="NULLABLE"),
        bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("link", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("street_address", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("business_phone", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("state", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("cik", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("zip_code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("irs_number", "INTEGER", mode="NULLABLE"),
    ]

    stock_comparison_schema = [
        bigquery.SchemaField("security_type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("change_in_shares", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("quarter_two_shares", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("filer_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("quarter_one_shares", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("filer_name", "STRING", mode="NULLABLE"),
    ]

    holdings_comparison_schema = [
        bigquery.SchemaField("quarter_two_market_value","INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("quarter_two_shares", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("change_in_shares", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("quarter_one_percent_of_portfolio", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("security_type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("stock_id", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("stock_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("quarter_one_shares", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField(
            "quarter_two_percent_of_portfolio", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("quarter_one_market_value", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("symbol", "STRING", mode="NULLABLE")
    ]

    holders_schema = [
        bigquery.SchemaField("stock_id", "INTEGER",	mode="NULLABLE"),
        bigquery.SchemaField("stock_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField(
            "records",
            "RECORD",
            mode="REPEATED",
            fields=[bigquery.SchemaField("quarter_id", "INTEGER", mode="NULLABLE"),
                    bigquery.SchemaField("quarter", "DATE", mode="NULLABLE"),
                    bigquery.SchemaField(
                "holdings",
                        "RECORD",
                        mode="REPEATED",
                        fields=[
                            bigquery.SchemaField(
                                "filer_state", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "filer_city", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "filer_street_address", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "percent_ownership", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "source_date", "DATE", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "stock_ticker", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "filer_name", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "quarter_id_owned", "INTEGER", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "avg_price", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "stock_id", "INTEGER", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "previous_shares", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "current_shares", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "shares_change", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "source", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "previous_mv", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "current_percent_of_portfolio", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "previous_percent_of_portfolio", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "current_mv", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "previous_ranking", "INTEGER", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "filer_zip_code", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "sector", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "current_ranking", "INTEGER", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "industry", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "position_change_type", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "stock_name", "STRING", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "filer_id", "INTEGER", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "percent_change", "FLOAT", mode="NULLABLE"),
                            bigquery.SchemaField(
                                "security_type", "STRING", mode="NULLABLE")
                        ],
            ),
            ],
        ),

    ]
