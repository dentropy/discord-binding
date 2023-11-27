from pprint import pprint
import pandas as pd
import timeit
import psycopg2
import psycopg2.extras

def query_resolver(pg_cursor, queries, query_name, query_args_dict = {}):
    for query in queries:
        if query["name"] == query_name:
            for arg in query["required_args"]:
                if arg not in list(query_args_dict.keys()):
                    return f"""
                        Error: Missing Query Args
                        Required Args: {str(query["required_args"])}
                        Provided Args: {str(list(query_args.keys()))}
                    """
            query_args = []
            for arg in query["arg_order"]:
                # print("arg")
                # print(arg)
                # print(query_args_dict[arg])
                # print("\n\n")
                query_args.append(query_args_dict[arg])
            start_time = timeit.default_timer()
            # print("query_args")
            # pprint(query_args)
            # print("\n\n")
            pg_cursor.execute(query["sql_query"], tuple(query_args))
            query_results = pg_cursor.fetchall()
            result_df = pd.DataFrame(query_results)
            elapsed = timeit.default_timer() - start_time
            # query_time_df = pd.concat([pd.DataFrame({
            #     "query_name" : "calculate_table_row_counts", 
            #     "time_in_seconds" : elapsed,
            #     "current_time" : pd.Timestamp.now()
            # }, index=[0]), self.query_time_df])
            return result_df