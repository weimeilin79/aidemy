import os
import json
from flask import Flask, render_template, request, jsonify, send_file, render_template_string
from aidemy import prep_class  

app = Flask(__name__)
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")


@app.route('/', methods=['GET', 'POST'])
def index():
    subjects = ['English', 'Mathematics', 'Science', 'Social Studies', 'Art', 'Music', 'Physical Education']
    years = list(range(5, 10))

    if request.method == 'POST':
        selected_year = int(request.form['year'])
        selected_subject = request.form['subject']
        addon_request = request.form['addon']

        teaching_plan = prep_class( 
            f"""For a year {selected_year} course on {selected_subject} covering {addon_request}, 
            Incorporate the school curriculum, 
            book recommendations, 
            and relevant online resources aligned with the curriculum outcome. 
            generate a highly detailed, day-by-day 3-week teaching plan, 
            send the teaching plan to the 'plan' topic 
            After sending to topic, return the teaching plan in markdown format
            """
        )
        return jsonify({'teaching_plan': teaching_plan})
    return render_template('index.html', years=years, subjects=subjects, teaching_plan=None, assignment=None)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
