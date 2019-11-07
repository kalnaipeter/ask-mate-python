from flask import Flask, render_template, request, redirect
from datetime import datetime
import data_handler

app = Flask(__name__)


@app.route('/')
def start():
    return redirect('/list')

@app.route('/list')
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

        data_handler.write_data('sample_data/question.csv', story)
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('list.html', stories=stories)
    else:
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('list.html', stories=stories)

@app.route('/question/<int:question_id>/new-answer')
@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def route_question(question_id=None):
    if request.method == "GET":
        result = []
        stories = data_handler.read_data('sample_data/answer.csv')
        for item in stories:
            if item["question_id"] == str(question_id):
                result.append(item)

        return render_template("answer.html", stories=result, question_id=question_id)

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    if request.method == "POST":
        story = {"id":"",
                 "submission_time": dt_string,
                 "vote_number": "",
                 "question_id": question_id,
                 "message": request.form.get("message"),
                 "image": ""
                 }
        data_handler.write_data('sample_data/answer.csv', story)
        stories = data_handler.read_data('sample_data/answer.csv')
        return render_template('answer.html', stories=stories,question_id=question_id)

@app.route('/question/<int:question_id>/add-new-answer')
def route_add_new_answer(question_id=None):
    return render_template("add-new-answer.html",question_id=question_id)

@app.route('/add-question')
def route_add_question():
    return render_template("add-question.html")

@app.route('/add_answer')
def route_add_answer():
    return render_template("add_answer.html")

@app.route("/upvoting/<int:story.id>")
def upvoting(story_id=None):


    story = {"id":"",
             "submission_time": "",
             "vote_number": request.form.get("vote_number"),
             "question_id": "",
             "message": "",
             "image": ""}
    data_handler.write_data('sample_data/question.csv', story)
    stories = data_handler.read_data('sample_data/question.csv')
    return render_template('answer.html', stories=stories, question_id=question_id)

@app.route("/downvoting/<int:question_id>")
def downvoting(question_id=None):
    votes = None
    stories = data_handler.read_data('sample_data/answer.csv')
    for story in stories:
        if story["id"] == str(question_id):
            votes = story["vote_number"]
            votes-=1

    data_handler.write_data('sample_data/question.csv', story)
    return render_template('answer.html', stories=stories, question_id=question_id)