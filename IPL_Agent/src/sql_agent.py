import os
from config.constants import MODEL_NAME
from config.prompt import generate_final_prompt
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from IPL_Agent.db.db_access import PostgresDB

db = PostgresDB()
connection_string = db.create_connection_string()

db = SQLDatabase.from_uri(connection_string)
print(db.dialect)
print(db.get_usable_table_names())
final_prompt = generate_final_prompt()
llm = ChatOpenAI(model= MODEL_NAME, temperature = 0)
agent_executor = create_sql_agent(llm, db=db, 
                                  agent_type="openai-tools", 
                                  verbose=True, prompt=final_prompt)
query_input = input("Please ask question related to IPL\n")
response = agent_executor.invoke({"input": query_input})
print(response)



