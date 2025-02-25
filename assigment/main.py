import os
import json
import base64
import random
from google.cloud import storage
import functions_framework

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from gemini import gen_assignment_gemini,combine_assignments
from deepseek import gen_assignment_deepseek
from typing import TypedDict

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
ASSIGNMENT_BUCKET = os.environ.get("ASSIGNMENT_BUCKET","")


class State(TypedDict):
    teaching_plan: str
    model_one_assignment: str
    model_two_assignment: str
    final_assignment: str

def create_assignment(teaching_plan: str):
    print(f"create_assignment---->{teaching_plan}")
    builder = StateGraph(State)
    builder.add_node("gen_assignment_gemini", gen_assignment_gemini)
    builder.add_node("gen_assignment_deepseek", gen_assignment_deepseek)
    builder.add_node("combine_assignments", combine_assignments)
    
    builder.add_edge(START, "gen_assignment_gemini")
    builder.add_edge("gen_assignment_gemini", "gen_assignment_deepseek")
    builder.add_edge("gen_assignment_deepseek", "combine_assignments")
    builder.add_edge("combine_assignments", END)

    graph = builder.compile()
    state = graph.invoke({"teaching_plan": teaching_plan})

    return state["final_assignment"]



@functions_framework.cloud_event
def generate_assignment(cloud_event):
    print(f"CloudEvent received: {cloud_event.data}")

    try:
        if isinstance(cloud_event.data.get('message', {}).get('data'), str): 
            data = json.loads(base64.b64decode(cloud_event.data['message']['data']).decode('utf-8'))
            teaching_plan = data.get('teaching_plan')
        elif 'teaching_plan' in cloud_event.data: 
            teaching_plan = cloud_event.data["teaching_plan"]
        else:
            raise KeyError("teaching_plan not found") 

        assignment = create_assignment(teaching_plan)

        print(f"Assignment---->{assignment}")

        #Store the return assignment into bucket as a text file
        storage_client = storage.Client()
        bucket = storage_client.bucket(ASSIGNMENT_BUCKET)
        file_name = f"assignment-{random.randint(1, 1000)}.txt"
        blob = bucket.blob(file_name)
        blob.upload_from_string(assignment)

        return f"Assignment generated and stored in {ASSIGNMENT_BUCKET}/{file_name}", 200

    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        print(f"Error decoding CloudEvent data: {e} - Data: {cloud_event.data}")
        return "Error processing event", 500

    except Exception as e:
        print(f"Error generate assignment: {e}")
        return "Error generate assignment", 500
