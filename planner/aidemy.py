import os
import random
import requests
import vertexai
from typing import TypedDict, Literal
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from curriculums import get_curriculum 
from search import search_latest_resource 
from book import recommend_book 




project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env

# Connect to resourse needed from Google Cloud
llm = ChatVertexAI(model_name="gemini-2.0-flash-001")



tools = [get_curriculum, search_latest_resource, recommend_book]

def determine_tool(state: MessagesState):

    sys_msg = SystemMessage(
                    content=(
                        "You are a helpful teaching assistant that help gathering all needed informations"
                    )
                )

    llm_with_tools = llm.bind_tools(tools)
    return {"messages": llm_with_tools.invoke([sys_msg] + state["messages"])} 



def prep_class(prep_needs):
   
    builder = StateGraph(MessagesState)
    builder.add_node("determine_tool", determine_tool)
    builder.add_node("tools", ToolNode(tools))
    
    builder.add_edge(START, "determine_tool")
    builder.add_conditional_edges("determine_tool",tools_condition)
    builder.add_edge("tools", "determine_tool")

    
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

    config = {"configurable": {"thread_id": "1"}}
    messages = graph.invoke({"messages": prep_needs},config)
    print(messages)
    for m in messages['messages']:
        m.pretty_print()
    teaching_plan_result = messages["messages"][-1].content  


    return teaching_plan_result# Return both



    



#prep_class("I'm doing a course for  year 5 on subject Mathematics in Geometry, , get school curriculum , and come up with few books recommendation plus  search latest resources on the internet base on the curriculum outcome. And come up with a 3 week teaching plan)")