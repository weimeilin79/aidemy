import os
import json
from flask import Flask, render_template, request, jsonify, send_file, render_template_string
from aidemy import prep_class  
from google.cloud import pubsub_v1

app = Flask(__name__)
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

#curl -X POST -F year=6 -F subject="Mathematics" -F addon="Geometry" http://127.0.0.1:8080/
@app.route('/', methods=['GET', 'POST'])
def index():
    subjects = ['English', 'Mathematics', 'Science', 'Social Studies', 'Art', 'Music', 'Physical Education']
    years = list(range(5, 10))

    if request.method == 'POST':
        selected_year = int(request.form['year'])
        selected_subject = request.form['subject']
        addon_request = request.form['addon']

        # Call prep_class to get teaching plan and assignment
        teaching_plan = prep_class(f"I'm doing a course for year {selected_year} on subject {selected_subject} in {addon_request}, get school curriculum, and come up with a few book recommendations plus search the latest resources on the internet based on the curriculum outcome. And come up with a 3-week teaching plan.")
        send_plan_event(teaching_plan)
        return jsonify({'teaching_plan': teaching_plan})
    return render_template('index.html', years=years, subjects=subjects, teaching_plan=None, assignment=None)



def send_plan_event(teaching_plan:str):
    publisher = pubsub_v1.PublisherClient()
    print(f"-------------> PROJECT_ID: {PROJECT_ID}")
    topic_path = publisher.topic_path(PROJECT_ID, "plan")

    message_data = {"teaching_plan": teaching_plan} 
    data = json.dumps(message_data).encode("utf-8") 

    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
    return "Published"




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
