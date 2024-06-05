import redis
from config.constants import MODEL_NAME
from config.prompt import generate_final_prompt
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from db.db_access import PostgresDB


# Function to get cached result or execute query if not cached
def get_query_response(query, redis_client):
    # Check if the result is in the cache
    cached_result = redis_client.get(query)
    if cached_result:
        print("Returning cached result")
        return cached_result.decode('utf-8')
    
    # Execute the query
    response = agent_executor.invoke({"input": query})
    
    # # Cache the result with an expiration time (optional, e.g., 300 seconds)
    redis_client.set(response['input'], response['output'])
    
    return response


# Prepopulate Redis with initial FAQs (if not already cached)
def populate_initial_faqs():
    faqs = {
        "What is the IPL?": "The Indian Premier League (IPL) is a professional Twenty20 cricket league in India.",
        "Who won the last IPL?": "The last IPL was won by Chennai Super Kings in 2023.",
        "When does the IPL season start?": "The IPL season typically starts in March or April and ends in May.",
        # Add more FAQs and answers here
    }
    for question, answer in faqs.items():
        if not redis_client.exists(question):
            redis_client.set(question, answer)







if __name__ == "__main__":
    # Initialize Redis client
    redis_client = redis.Redis(host='localhost', port=6375, db=0)
    # Database connection
    db = PostgresDB()
    connection_string = db.create_connection_string()

    db = SQLDatabase.from_uri(connection_string)
    print(db.dialect)
    print(db.get_usable_table_names())
    final_prompt = generate_final_prompt()
    llm = ChatOpenAI(model=MODEL_NAME, temperature=0)
    agent_executor = create_sql_agent(llm, db=db, 
                                    agent_type="openai-tools", 
                                    verbose=True, prompt=final_prompt)
    
    # Populate initial FAQs
    populate_initial_faqs()

    while True:

        # Get user query input
        query_input = input("Please ask a question related to IPL\n")
        # Get the response, either from cache or by executing the query
        response = get_query_response(query_input, redis_client)
        print(response)
        if query_input == "exit":
            break


