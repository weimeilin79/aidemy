import functions_framework
import json
from flask import Flask, jsonify, request
from langchain_google_vertexai import ChatVertexAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
import os

#functions-framework --target recommended  --source provider.py
#curl -X POST -H "Content-Type: application/json" -d '{"category": "Science Fiction", "number_of_book": 2}' http://localhost:8080/
#curl -X POST -H "Content-Type: application/json" -d '{"category": "Science Fiction", "number_of_book": 2}' https://us-central1-named-icon-449202-s9.cloudfunctions.net/hello-world

class Book(BaseModel):
    bookname: str = Field(description="Name of the book")
    author: str = Field(description="Name of the author")
    publisher: str = Field(description="Name of the publisher")
    publishing_date: str = Field(description="Date of publishing")

# ENV SETUP
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env

# Connect to resourse needed from Google Cloud
llm = ChatVertexAI(model_name="gemini-2.0-flash-001")

def get_recommended_books(category):
    """
    A simple book recommendation function. 

    Args:
        category (str): category

    Returns:
        str: A JSON string representing the recommended books.
    """
    parser = JsonOutputParser(pydantic_object=Book)
    question = f"Generate a book recommendation on {category} with bookname, author and publisher and publishing_date"

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    chain = prompt | llm | parser
    response = chain.invoke({"query": question})

    return  json.dumps(response)
    

@functions_framework.http
def recommended(request):
    request_json = request.get_json(silent=True) # Get JSON data
    if request_json and 'category' in request_json and 'number_of_book' in request_json:
        category = request_json['category']
        number_of_book = int(request_json['number_of_book'])
    elif request.args and 'category' in request.args and 'number_of_book' in request.args:
        category = request.args.get('category')
        number_of_book = int(request.args.get('number_of_book'))

    else:
        return jsonify({'error': 'Missing category or number_of_book parameters'}), 400


    recommendations_list = []
    for i in range(number_of_book):
        book_dict = json.loads(get_recommended_books(category))
        print(f"book_dict=======>{book_dict}")
    
        recommendations_list.append(book_dict)

    
    return jsonify(recommendations_list)
