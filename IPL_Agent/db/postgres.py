import pandas as pd
from sqlmodel import Session
from sqlalchemy import delete
from db.db_access import PostgresDB
from db.models import IPL_MatchData, IPL_MatchInfo
from utils.enums import TableName

def insert_into_postgres(data):
    db_obj = PostgresDB()
    engine = db_obj.connect_to_db()
    try:
        with Session(engine) as session:
            for row in data:
                try:
                    ## Insert the object into the database
                    session.add(row)
                    session.commit()
                except Exception as e:
                    # Integrity constraint violations (e.g., duplicate primary keys)
                    session.rollback()
                    print(f"Failed to insert row: {row}. Exception: {e}")
    except Exception as e:
        # Handle exceptions related to database connection or session creation
        print(f'Failed to connect to database or session. Error: {e}')


def delete_user_data(table_name):
    db_obj = PostgresDB()
    engine = db_obj.connect_to_db()
    with Session(engine) as session:
        if table_name == TableName.MATCHDATA:
            statement = delete(IPL_MatchData)
        elif table_name == TableName.MATCHINFO:
            statement = delete(IPL_MatchInfo)
        session.exec(statement)
        session.commit()
        print(f"Deleted user data from table successfully")

