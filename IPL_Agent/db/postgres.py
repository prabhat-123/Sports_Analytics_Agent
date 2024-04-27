# import pandas as pd
# from sqlmodel import Field, Session, SQLModel, create_engine, select
# from db.models import (
#     IPL_MatchData,
#     IPL_MatchInfo
# )
# from sqlalchemy import delete




# def run_sql_query(connection, sql_query)->Tuple[bool, dict]:
#     """
#         Executes the SQL Query. 
#         Returns <SUCCESS, OUTPUT>
#     """
#     # Status of SQL execution
#     status = False
#     output = None

#     print("Running SQL query")
#     try:
#         with connection.cursor(row_factory=dict_row) as cursor:
#             cursor.execute(sql_query)

#             # Fetch the results
#             results = cursor.fetchall()
            
#             df = pd.DataFrame(results)

#             if results:
#                 df.columns = [key for key in results[0].keys()]
#                 output = df.to_dict("list")
            
#             status = True

#     except psycopg.Error as e:
#         connection.rollback()  # Rollback the transaction in case of an error
#         print(f"Error: {e}. Rolling Back")
#         output = {"error" : e}

#     finally:
#         if 'cursor' in locals() and cursor is not None:
#             cursor.close()

#     return status, output




# def delete_user_data(user_id: str):
#     print("Now starting Table Deletion")
#     for i in range(1,14):
#         table_name = f"Section_{i}"
#         Section: Section_1 = globals().get(table_name)
#         if not Section:
#             continue
#         with Session(engine) as session:
#             statement = delete(Section).where(Section.tenant==user_id)
#             session.exec(statement)
#             session.commit()
#             print(f"Deleted {user_id} info from Table {Section.__name__}")
    

#     print("Finished Deleting tables")


# def insert_into_postgres(data, user_id:str):
#     session = Session(engine)
#     # For each SDS
#     for key, section in data.items():
#         print("SDS NAME : ", key)
#         valid_for_insertion = "SEC_1" in list(section.keys()) and section["SEC_1"].get('substance_name')

#         # Avoid insertion
#         if not valid_for_insertion:
#             continue

#         for name, values in section.items():
#             try:
#                 section_number = int(name.split('_')[1])
#                 model_name = f'Section_{section_number}'
#                 Section = globals()[model_name] 
#             except Exception as e:
#                 print(f"Model : {name} not yet Created !")
#                 continue

#             if not values:
#                 print("Values Empty for ", name)
#                 continue
#             print("Adding data for  Section ", name)
#             # TODO This is redundant for tables except section-1. However it's not working now.
#             values['tenant'] = user_id
#             values['substance_name'] = key
#             row = Section(**values)
#             session.add(row)

#         try:
#             session.commit()
#         except Exception as e:
#             print(" *********** Error : ", e)
#             session.rollback()
#             print("Skipped Insertion for SDS : ", key)

#     print("Now committing Sessions !")
#     session.close()


# # Function to get last_access_time from the database
# def get_last_access_time_from_db(connection, user: str):
#     with connection.cursor() as cursor:
#         cursor.execute(
#             sql.SQL("SELECT last_access_time FROM user_last_access WHERE tenant = {}").format(sql.Literal(user))
#         )
#         result = cursor.fetchone()
#     if result:
#         return result[0]
#     else:
#         # Handle the case when the user does not exist in the database
#         return None

# # Function to update last_access_time in the database
# def update_last_access_time_in_db(connection ,user: str, current_time):
#     with connection.cursor() as cursor:
#         cursor.execute(
#             sql.SQL("""
#                 INSERT INTO user_last_access (tenant, last_access_time)
#                 VALUES ({}, {})  
#                 ON CONFLICT (tenant) DO UPDATE SET last_access_time = EXCLUDED.last_access_time
#             """).format(sql.Literal(user), sql.Literal(current_time))
#         )
#     connection.commit()


# def create_last_access_time_table(connection):
#     '''
#         This table stores last request date for given users. 
#     '''
#     print("Creating User access time table.")
#     create_table_query = sql.SQL("""CREATE TABLE IF NOT EXISTS user_last_access (
#                 id SERIAL PRIMARY KEY,
#                 tenant VARCHAR(255) UNIQUE NOT NULL,
#                 last_access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             );""")
    
#     with connection.cursor() as cursor:
#         cursor.execute(create_table_query)

#     connection.commit()

# def psycopg_connect_to_postgres(
#         DATABASE_URL: str, 
#         max_attempts=6, 
#         retry_timeout=15,
#     ):

#     DATABASE_URL = str(DATABASE_URL)
#     print("Database URL : ", DATABASE_URL)
#     # Counter for attempts
#     attempt = 1

#     while attempt <= max_attempts:
#         try:
#             # Attempt to make the connection
#             connection = psycopg.connect(DATABASE_URL)
#             print("Connection Sucess")
#             return connection
        
#         except psycopg.OperationalError as e:
#             # Handle the specific exception for connection issues
#             print(f"Attempt {attempt} failed: {e}")

#             # Increment the attempt counter
#             attempt += 1

#             # If it's not the last attempt, wait before the next try
#             if attempt <= max_attempts:
#                 print(f"Retrying in {retry_timeout} seconds...")
#                 time.sleep(retry_timeout)
#             else:
#                 print("Maximum retry attempts reached. Exiting.")
#                 # You might want to raise the exception or handle it accordingly
#                 raise
