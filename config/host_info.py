from utils.query import query_root_user_info,query_server_info

# tidb_password = query_server_info[0]

host_info_url = 'http://web-app.'+query_server_info()[1]
host_info_header = {
        "content-type": "application/json",
        "tenantid": query_root_user_info()[1],
        "userid": str(query_root_user_info()[0])
    }