import json
import os
from langchain_google_vertexai import VertexAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

class QuizQuestion(BaseModel):
    question: str = Field(description="The question itself")
    options: list[str] = Field(description="List of options", min_items=4, max_items=4)
    answer: str = Field(description="The correct answer letter (A, B, C, or D)")


# ENV SETUP
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env



def generate_quiz_question(file_name: str, difficulty: str, region:str ):
    """Generates a single multiple-choice quiz question using the LLM.
   
    ```json
    {
      "question": "The question itself",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct answer letter (A, B, C, or D)"
    }
    ```
    """

    print(f"region: {region}")
    # Connect to resourse needed from Google Cloud
    llm = VertexAI(model_name="gemini-1.5-pro", location=region)


    plan=None
    #load the file using file_name and read content into string call plan
    with open(file_name, 'r') as f:
        plan = f.read()

    parser = JsonOutputParser(pydantic_object=QuizQuestion)


    instruction = f"You'll provide one question with difficulty level of {difficulty}, 4 options as multiple choices and provide the anwsers, the quiz needs to be related to the teaching plan {plan}"

    prompt = PromptTemplate(
        template="Generates a single multiple-choice quiz question\n {format_instructions}\n  {instruction}\n",
        input_variables=["instruction"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    response = chain.invoke({"instruction": instruction})

    print(f"{response}")
    return  response


