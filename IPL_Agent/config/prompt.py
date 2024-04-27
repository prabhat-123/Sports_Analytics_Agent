import json
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.embeddings.azure_openai import AzureOpenAIEmbeddings
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import (
    FewShotPromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
from typing import cast


 
 
SQL_PREFIX = """
You are a {dialect} Expert. Given an input questions, first create a syntactically correct POSTGRES SQL query to run, then look at the results of the query and return the answer to the input question.
You can order the results to return the most informative data in the database. USE DISTINCT keyword to avoid duplicate rows in the result set.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
You MUST Use LIKE operator for pattern matching on all columns. DO NOT LIE. If the answer is not in the database, return a negative response to the user's query.
DO NOT generate the response from your knowledge base you are trained on for the factual contents that need to be taken from the external source. If the question is not clear, ask for more information.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
 
## SCHEMA INFORMATION
TABLE NAME: ipl_stats
Here are additional Information related to columns present in this column:
City: The city where the cricket match took place.
Date: The date on which the cricket match was held.
Season: The season or year in which the cricket match occurred.
MatchNumber: The unique identifier or number assigned to the match.
Team1: The name of the first cricket team participating in the match.
Team2: The name of the second cricket team participating in the match.
Venue: The venue or location where the cricket match was held.
TossWinner: The team that won the toss before the match.
TossDecision: The decision made by the team winning the toss (batting or bowling).
SuperOver: Indicates whether a Super Over (tie-breaker) was played in case of a tie.
WinningTeam: The name of the team that won the match.
WonBy: The margin or difference by which the winning team won the match (e.g., runs, wickets).
Margin: Additional information about the margin of victory (e.g., runs, wickets).
Method: Method of determining the winner (e.g., D/L method in case of rain-affected matches).
Player_of_Match: The player from the winning team who was awarded the "Man of the Match" award.
Team1Players: List of players from Team1 participating in the match.
Team2Players: List of players from Team2 participating in the match.
Umpire1: The name of the first umpire officiating the match.
Umpire2: The name of the second umpire officiating the match.
 
"""
 
SQL_SUFFIX = """Begin!

Question: {input}
Thought: I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
{agent_scratchpad}"""

SQL_FUNCTIONS_SUFFIX = """I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables."""

 
def generate_final_prompt(**kwargs):

    messages = [
        SystemMessage(content=cast(str, SQL_PREFIX)),
        HumanMessagePromptTemplate.from_template("{input}"),
        AIMessage(content=SQL_SUFFIX or SQL_FUNCTIONS_SUFFIX),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
    full_prompt = ChatPromptTemplate.from_messages(messages)
    return full_prompt
 
 
