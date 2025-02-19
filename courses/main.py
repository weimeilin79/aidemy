import os
import json
import base64
from google.cloud import pubsub_v1, storage
import functions_framework
from audio import breakup_sessions 

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
COURSE_BUCKET_NAME = os.environ.get("COURSE_BUCKET_NAME", "")


@functions_framework.cloud_event
def process_teaching_plan(cloud_event):
    print(f"CloudEvent received: {cloud_event.data}")

    try:
        if isinstance(cloud_event.data.get('message', {}).get('data'), str):  # Check for base64 encoding
            data = json.loads(base64.b64decode(cloud_event.data['message']['data']).decode('utf-8'))
            teaching_plan = data.get('teaching_plan') # Get the teaching plan
        elif 'teaching_plan' in cloud_event.data: # No base64
            teaching_plan = cloud_event.data["teaching_plan"]
        else:
            raise KeyError("teaching_plan not found") # Handle error explicitly

        #Load the teaching_plan as string and from cloud event, call audio breakup_sessions
        breakup_sessions(teaching_plan)

        storage_client = storage.Client()
        bucket = storage_client.bucket(COURSE_BUCKET_NAME)
        blob = bucket.blob("teaching_plan.txt")
        blob.upload_from_string(teaching_plan)

        print(f"Teaching plan saved to GCS: gs://{COURSE_BUCKET_NAME}/teaching_plan.txt")
        return "Teaching plan processed successfully", 200

    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        print(f"Error decoding CloudEvent data: {e} - Data: {cloud_event.data}")
        return "Error processing event", 500

    except Exception as e:
        print(f"Error processing teaching plan: {e}")
        return "Error processing teaching plan", 500
