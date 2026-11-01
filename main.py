import os

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights


import streamlit as st

# 1. Bridge Streamlit Cloud secrets FIRST
if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
if hasattr(st, "secrets") and "Tavily_API_key" in st.secrets:
    os.environ["Tavily_API_key"] = st.secrets["Tavily_API_key"]
if hasattr(st, "secrets") and "Database_URL" in st.secrets:
    os.environ["Database_URL"] = st.secrets["Database_URL"]

# 2. Now read Database_URL AFTER secrets are bridged
Database_URL = os.getenv("Database_URL")

# 3. Initialize LLM
llm = ChatGroq(model="openai/gpt-oss-120b")

class TravelState(TypedDict):
    message: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int
    
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return{
        "flight_results": flight_data,
        "message":[
            AIMessage(content=f"Flight search fetched")
        ]
    }
    
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state["user_query"]}"
    hotel_results = tavily_search(query)
    return{
        "hotel_results": hotel_results,
        "message":[
            AIMessage(content=f"Hotel search fetched")
        ]
    }
    
def itinerary_agent(state: TravelState):
    prompt = f"""
    Create a travel itinerary.
    User Query: {state["user_query"]}
    Flight Results: {state["flight_results"]}
    Hotel Results: {state["hotel_results"]}
    
    """
    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner."), 
        HumanMessage(content=prompt)
    ])
    
    return{
        
        "itinerary": response.content,
        "message":[response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
    
def final_agent(state: TravelState):
    final_prompt = f"""
    General final travel response.
    
    Flight: {state["flight_results"]}
    Hotel: {state["hotel_results"]}
    Itinerary: {state["itinerary"]}
    """
    
    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])
    
    return{
        "message":[response],
            "llm_calls": state.get("llm_calls", 0) + 1
    }
    
graph = StateGraph(TravelState)

#add nodes
graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

#workflow
graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)

#connect langrapg to postgres
# Try connecting to PostgreSQL; fallback to MemorySaver if unavailable on cloud
try:
    _conn = psycopg.connect(Database_URL, autocommit=True)
    checkpointer = PostgresSaver(_conn)
    checkpointer.setup()
except Exception as e:
    from langgraph.checkpoint.memory import MemorySaver
    checkpointer = MemorySaver()

#Use Database to store/save conversation
app = graph.compile(checkpointer=checkpoint)

#Thread_id(save partcular user previous conversation)
if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_Arooj123"
        }
    }
#get user input via terminal    
    user_query = input("Enter your travel query: ") 
    
    result = app.invoke(
        {
            "message": [
                HumanMessage(content=user_query)
            ],
            "user_query": user_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )
    
    print("\nFinal Response:\n")
    
    for msg in result["message"]:
        print(msg.content)
    