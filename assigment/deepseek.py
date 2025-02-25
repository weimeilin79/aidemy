import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from typing import TypedDict

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "")


class State(TypedDict):
    teaching_plan: str
    model_one_assignment: str
    model_two_assignment: str
    final_assignment: str

def gen_assignment_deepseek(state):
    print(f"---------------gen_assignment_deepseek")

    template = """
        You are an instructor who favor student to focus on individual work.

        Develop engaging and practical assignments for each week, ensuring they align with the teaching plan's objectives and progressively build upon each other.  

        For each week, provide the following:

        * **Week [Number]:** A descriptive title for the assignment (e.g., "Data Exploration Project," "Model Building Exercise").
        * **Learning Objectives Assessed:** List the specific learning objectives from the teaching plan that this assignment assesses.
        * **Description:** A detailed description of the task, including any specific requirements or constraints.  Provide examples or scenarios if applicable.
        * **Deliverables:** Specify what students need to submit (e.g., code, report, presentation).
        * **Estimated Time Commitment:**  The approximate time students should dedicate to completing the assignment.
        * **Assessment Criteria:** Briefly outline how the assignment will be graded (e.g., correctness, completeness, clarity, creativity).

        The assignments should be a mix of individual and collaborative work where appropriate.  Consider different learning styles and provide opportunities for students to apply their knowledge creatively.

        Based on this teaching plan: {teaching_plan}
        """

    
    prompt = ChatPromptTemplate.from_template(template)

    model = OllamaLLM(model="deepseek-r1:1.5b",
                   base_url=OLLAMA_HOST)

    chain = prompt | model


    response = chain.invoke({"teaching_plan":state["teaching_plan"]})
    state["model_two_assignment"] = response
    
    return state
