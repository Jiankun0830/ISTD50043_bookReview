import time

def add_log(query_type, query, response, user_id, user_type, mg):
    # following the type: time_stamp, query_type, query_info, answer, user_name, user_type
    time_stamp = time.time()
    to_insert = {
        "time_stamp": time_stamp,
        "query_type": query_type,
        "query": query,
        "response": response,
        "user_id": str(user_id),
        "user_type": user_type
    }
    mg.insert_query(to_insert)
