import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
CSV_DATA_PATH = './data/IPL_Matches_2008_2022.csv'
POSTGRES_TABLE = os.getenv('POSTGRES_TABLE')
MODEL_NAME = "gpt-3.5-turbo"



