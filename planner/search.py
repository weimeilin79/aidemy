import os
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from onramp_workaround import get_next_region

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")  # Get project ID from env

model_id = "gemini-2.0-flash-001"

google_search_tool = Tool(
    google_search = GoogleSearch()
)

def search_latest_resource(search_text: str, curriculum: str, subject: str, year: int):
    """
    Get latest information from the internet
    
    Args:
        search_text: User's request category   string
        subject: "User's request subject" string
        year: "User's request year"  integer
    """
    search_text = "%s in the context of year %d and subject %s with following curriculum detail %s " % (search_text, year, subject, curriculum)
    region = get_next_region()
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=region)
    print(f"search_latest_resource text-----> {search_text}")
    response = client.models.generate_content(
        model=model_id,
        contents=search_text,
        config=GenerateContentConfig(
            tools=[google_search_tool],
            response_modalities=["TEXT"],
        )
    )
    print(f"search_latest_resource response-----> {response}")
    return response
