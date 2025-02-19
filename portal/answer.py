import json
import os
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage


llm = VertexAI(model_name="gemini-2.0-flash-thinking-exp-01-21")
#llm = VertexAI(model_name="gemini-2.0-flash-001")

def answer_thinking(question, options, correct_answer):
    try:
        
       
        input_msg = HumanMessage(content=[f"Here the question{question}, here are the avalible options {options}, this was the correct answer {correct_answer}"])
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        "You are a helpful teacher trying to teach the student on question, you were given the question and a set of mutiple choices "
                        "Explain in detail how to come up with the answer, and why does each options are not correct."
                        
                    )
                ),
                input_msg,
            ]
        )

        prompt = prompt_template.format()
        
        response = llm.invoke(prompt)
        print(f"response: {response}")

        return response
    except Exception as e:
        print(f"Error sending message to chatbot: {e}") # Log this error too!
        return f"Unable to process your request at this time. Due to the following reason: {str(e)}"