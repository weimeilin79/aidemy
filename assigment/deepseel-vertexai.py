import os
import vertexai
from typing import TypedDict
from google.cloud import aiplatform

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
ENDPOINT_ID = os.environ.get("DS_ENDPOINT_ID", "") 
PROJECT_NUMBER= os.environ.get("GOOGLE_CLOUD_PROJECT_NUMBER", "") 


class State(TypedDict):
    teaching_plan: str
    model_one_assignment: str
    model_two_assignment: str
    final_assignment: str

aiplatform.init(project=PROJECT_ID, location=LOCATION)
endpoint = aiplatform.Endpoint(f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/endpoints/{ENDPOINT_ID}")

def gen_assignment_deepseek(state):
    print(f"---------------gen_assignment_deepseek")

    
    instances=[{
              "prompt" : f"""
        You are an instructor 

        Develop engaging and practical assignments for each week, ensuring they align with the teaching plan's objectives and progressively build upon each other.  

        For each week, provide the following:

        * **Week [Number]:** A descriptive title for the assignment (e.g., "Data Exploration Project," "Model Building Exercise").
        * **Learning Objectives Assessed:** List the specific learning objectives from the teaching plan that this assignment assesses.
        * **Description:** A detailed description of the task, including any specific requirements or constraints.  Provide examples or scenarios if applicable.
        * **Deliverables:** Specify what students need to submit (e.g., code, report, presentation).
        * **Estimated Time Commitment:**  The approximate time students should dedicate to completing the assignment.
        * **Assessment Criteria:** Briefly outline how the assignment will be graded (e.g., correctness, completeness, clarity, creativity).

        The assignments should be a mix of individual and collaborative work where appropriate.  Consider different learning styles and provide opportunities for students to apply their knowledge creatively.

        Based on this teaching plan: {state["teaching_plan"]}
        """,
              "max_tokens": 2000,
              "temperature": 0.7,
              "top_p": 1.0,
              "top_k": -1
    }]
    

   

    prediction = endpoint.predict(instances=instances, use_dedicated_endpoint=True)
    print(prediction.predictions[0])
   

    
    
    state["model_two_assignment"] = prediction.predictions[0]
    
    return state
