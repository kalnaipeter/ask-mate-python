from flask import Flask, render_template, request, redirect
from datetime import datetime
import data_handler

app = Flask(__name__)


@app.route('/')
def start():
    return redirect('/list')


@app.route('/list', methods=["GET", "POST"])
def route_main():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    if request.method == "POST":
        story = {"id": "3",
                 "submission_time": dt_string,
                 "view_number": "0",
                 "vote_number": "0",
                 "title": request.form.get("title"),
                 "message": request.form.get("message"),
                 "image": ""
                 }
        print(story)
        data_handler.write_data('sample_data/question.csv', story)
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('list.html', stories=stories)
    else:
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('list.html', stories=stories)


@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def route_question(question_id=None):
    if request.method == "GET":
        result = []
        stories = data_handler.read_data('sample_data/answer.csv')
        for item in stories:
            if item["question_id"] == str(question_id):
                result.append(item)

        return render_template("answer.html", stories=result)


@app.route('/add-question')
def route_add_question():
    return render_template("add-question.html")


if __name__ == "__main__":
    app.run(debug=True)
