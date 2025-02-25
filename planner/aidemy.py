import os
import random
import requests
import vertexai
import json
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
from onramp_workaround import get_next_region

from google.cloud import pubsub_v1


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env

def send_plan_event(teaching_plan:str):
    """
    Send the teaching event to the topic called plan
    
    Args:
        teaching_plan: teaching plan
    """
    publisher = pubsub_v1.PublisherClient()
    print(f"-------------> Sending event to topic plan: {teaching_plan}")
    topic_path = publisher.topic_path(PROJECT_ID, "plan")

    message_data = {"teaching_plan": teaching_plan} 
    data = json.dumps(message_data).encode("utf-8") 

    future = publisher.publish(topic_path, data)

    return f"Published message ID: {future.result()}"

tools = [get_curriculum, search_latest_resource, recommend_book,send_plan_event]

def determine_tool(state: MessagesState):
    llm = ChatVertexAI(model_name="gemini-2.0-flash-001", location=get_next_region())
    sys_msg = SystemMessage(
                    content=(
                        f"""You are a helpful teaching assistant that helps gather all needed information. 
                            Your ultimate goal is to create a detailed 3-week teaching plan. 
                            You have access to tools that help you gather information.  
                            Based on the user request, decide which tool(s) are needed. 

                        """
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


    return teaching_plan_result
