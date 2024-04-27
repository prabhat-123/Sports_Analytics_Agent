import sqlalchemy as sa
import pandas as pd
from config.constants import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_HOST,
    POSTGRES_PORT,
    CSV_DATA_PATH,
    POSTGRES_TABLE,
    POSTGRES_PASSWORD
)

class PostgresDB:
    def __init__(self):
        self.csv_path = CSV_DATA_PATH
        self.db_name = POSTGRES_DB
        self.db_user = POSTGRES_USER
        self.db_password = POSTGRES_PASSWORD
        self.db_host = POSTGRES_HOST
        self.db_port = POSTGRES_PORT
        self.table = POSTGRES_TABLE
        self.engine = None

    def create_connection_string(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    def connect_to_db(self):
        connection_string = self.create_connection_string()
        self.engine = sa.create_engine(connection_string)
        return self.engine

    # def insert_data_into_db(self):
    #     if self.engine is None:
    #         raise Exception("Database connection not initialized. Call connect_to_db() first.")
        
    #     df = pd.read_csv(self.csv_path)
        # df.to_sql(self.table, self.engine, schema="", if_exists='replace')


