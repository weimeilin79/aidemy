import os
import json
import asyncio
import wave 
import time

import functions_framework
import soundfile as sf
from google import genai
from google.cloud import storage  
from google.genai.types import (
    Content,
    LiveConnectConfig,
    SpeechConfig,
    VoiceConfig,
    PrebuiltVoiceConfig,
    Part,
)

MODEL_ID = "gemini-2.0-flash-exp"
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
BUCKET_NAME = os.environ.get("COURSE_BUCKET_NAME", "")


config = LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=SpeechConfig(
        voice_config=VoiceConfig(
            prebuilt_voice_config=PrebuiltVoiceConfig(
                voice_name="Charon",
            )
        )
    ),
)

async def process_weeks(teaching_plan: str):
    region = "us-west1" #To workaround onRamp qouta limits
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=region)
    
    clientAudio = genai.Client(vertexai=True, project=PROJECT_ID, location="us-central1")
    async with clientAudio.aio.live.connect(
        model=MODEL_ID,
        config=config,
    ) as session:
        for week in range(1, 4):  
            response = client.models.generate_content(
                model="gemini-1.0-pro",
                contents=f"Given the following teaching plan: {teaching_plan}, Extrace content plan for week {week}. And return just the plan, nothingh else  " # Clarified prompt
            )

            prompt = f"""
                Assume you are the instructor.  
                Prepare a concise and engaging recap of the key concepts and topics covered. 
                This recap should be suitable for generating a short audio summary for students. 
                Focus on the most important learnings and takeaways, and frame it as a direct address to the students.  
                Avoid overly formal language and aim for a conversational tone, tell a few jokes. 
                
                Teaching plan: {response.text} """
            print(f"prompt --->{prompt}")

            await session.send(input=prompt, end_of_turn=True)
            with open(f"temp_audio_week_{week}.raw", "wb") as temp_file:
                async for message in session.receive():
                    if message.server_content.model_turn:
                        for part in message.server_content.model_turn.parts:
                            if part.inline_data:
                                temp_file.write(part.inline_data.data)
                            
            data, samplerate = sf.read(f"temp_audio_week_{week}.raw", channels=1, samplerate=24000, subtype='PCM_16', format='RAW')
            sf.write(f"course-week-{week}.wav", data, samplerate)
        
            storage_client = storage.Client()
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(f"course-week-{week}.wav")  # Or give it a more descriptive name
            blob.upload_from_filename(f"course-week-{week}.wav")
            print(f"Audio saved to GCS: gs://{BUCKET_NAME}/course-week-{week}.wav")
    await session.close()

 
def breakup_sessions(teaching_plan: str):
    asyncio.run(process_weeks(teaching_plan))
