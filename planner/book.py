import os
import requests
from langchain_google_vertexai import VertexAI


# Connect to resourse needed from Google Cloud
llm = VertexAI(model_name="gemini-2.0-flash-001")

def recommend_book(query: str):
    """
    Get a list of recommended book from an API endpoint
    
    Args:
        query: User's request string
    """

    query = f"""The user is trying to plan a education course, you are the teaching assistant. Help define the category of what the user requested to teach, respond the categroy with no more than two word.

    user request:   {query}
    """
    print(f"-------->{query}")
    response = llm.invoke(query)
    print(f"CATEGORY RESPONSE------------>: {response}")
    
    # call this using python and parse the json back to dict -H "Content-Type: application/json" -d '{"categrory": "Science Fiction", "number_of_book": 2}' https://us-central1-named-icon-449202-s9.cloudfunctions.net/hello-world
    category = response.strip()

    url = "https://us-central1-named-icon-449202-s9.cloudfunctions.net/book-provider"
    headers = {"Content-Type": "application/json"}
    data = {"category": category, "number_of_book": 3}
    print(f"Request Data: {data}")  # Print the exact request
    books = requests.post(url, headers=headers, json=data)

    print(f"Response Status Code: {books.status_code}")  # Check status code
    print(f"Response Text: {books.text}")  # Print the response body
   
    return books.text
 
#recommand_book("I'm doing a course for my 5th grade student on Math Geometry, I'll need to recommand few books come up with a teach plan, few quizes and also a homework assignment.")
