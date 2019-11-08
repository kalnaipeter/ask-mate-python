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
        story = {"id": request.form.get("question_id") if request.form.get("question_id") is not None else "",
                 "submission_time": dt_string,
                 "view_number": "0",
                 "vote_number": "0",
                 "title": request.form.get("title"),
                 "message": request.form.get("message"),
                 "image": ""
                 }

        data_handler.write_data('sample_data/question.csv', story)
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('questions.html', stories=stories)
    else:
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('questions.html', stories=stories)

@app.route('/question/<int:question_id>/new-answer')
@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def route_question(question_id=None):
    if request.method == "GET":
        questions = data_handler.read_data('sample_data/question.csv')
        question_title = None
        for item in questions:
            if item["id"] == str(question_id):
                question_title = item["title"]
        result = []
        stories = data_handler.read_data('sample_data/answer.csv')
        for item in stories:
            if item["question_id"] == str(question_id):
                result.append(item)

        return render_template("answer.html", stories=result, question_id=question_id,question_title=question_title)

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

        questions = data_handler.read_data('sample_data/question.csv')
        question_title = None
        for item in questions:
            if item["id"] == str(question_id):
                question_title = item["title"]
        data_handler.write_data('sample_data/answer.csv', story)
        result = []
        stories = data_handler.read_data('sample_data/answer.csv')
        for item in stories:
            if item["question_id"] == str(question_id):
                result.append(item)

        return render_template("answer.html", stories=result, question_id=question_id,question_title=question_title)
        # stories = data_handler.read_data('sample_data/answer.csv')
        # return render_template('answer.html', stories=stories,question_id=question_id)


@app.route('/question/<int:question_id>/add-new-answer')
def route_add_new_answer(question_id=None):
    return render_template("add-new-answer.html", question_id=question_id)


@app.route('/question/<int:question_id>/edit', methods=["GET","POST"])
@app.route('/add-question')
def route_add_question(question_id=None):
    if request.method == "GET":
        if question_id is not None:
            question_title = None
            question_message = None
            stories = data_handler.read_data("sample_data/question.csv")
            for story in stories:
                if str(question_id) == story["id"]:
                    question_title = story["title"]
                    question_message= story["message"]

            return render_template("add-question.html", question_id=question_id,question_message=question_message,question_title=question_title)
        else:
            return render_template("add-question.html")
#
# @app.route("/upvoting/<int:question_id>")
# def upvoting(question_id=None):
#     story = {"id": "",
#              "submission_time": "",
#              "view_number": "",
#              "vote_number": "",
#              "title": "",
#              "message": "",
#              "image": ""}
#
#     stories = data_handler.read_data("sample_data/question.csv")
#     for item in stories:
#         if item["id"] == str(question_id):
#             story["vote_number"] = str(int(item["vote_number"]) + 1)
#             story["id"] = item["id"]
#             story["submission_time"] = item["submission_time"]
#             story["view_number"] = item["view_number"]
#             story["title"] = item["title"]
#             story["message"] = item["message"]
#             story["image"] = item["image"]
#
#     data_handler.write_data('sample_data/question.csv', story)
#     stories = data_handler.read_data('sample_data/question.csv')
#     return render_template('questions.html', stories=stories)
#
# @app.route("/downvoting/<int:question_id>")
# def downvoting(question_id=None):
#     story = {"id": "",
#              "submission_time": "",
#              "view_number":  "",
#              "vote_number": "",
#              "title": "",
#              "message": "",
#              "image":  ""}
#
#     stories = data_handler.read_data('sample_data/question.csv')
#     for item in stories:
#         if item["id"] == str(question_id):
#             story["vote_number"]=str(int(item["vote_number"])-1)
#             story["id"] = item["id"]
#             story["submission_time"] = item["submission_time"]
#             story["view_number"] = item["view_number"]
#             story["title"] = item["title"]
#             story["message"] = item["message"]
#             story["image"] = item["image"]
#
#     data_handler.write_data('sample_data/question.csv', story)
#     stories = data_handler.read_data('sample_data/question.csv')
#     return render_template('questions.html', stories=stories)
#
# @app.route("/answer_upvoting/<int:question_id>")
# def answerupvoting(question_id=None):
#     story = {"id": "",
#              "submission_time": "",
#              "vote_number": "",
#              "question_id": "",
#              "message": "",
#              "image":  ""}
#
#     print(story)
#     stories = data_handler.read_data('sample_data/answer.csv')
#     print(stories)
#     for item in stories:
#         if item["id"] == str(question_id):
#             story["vote_number"]=str(int(item["vote_number"])+1)
#             story["id"] = item["id"]
#             story["submission_time"] = item["submission_time"]
#             story["question_id"] = item["question_id"]
#             story["message"] = item["message"]
#             story["image"] = item["image"]
#
#     data_handler.write_data('sample_data/answer.csv', story)
#     result = []
#     stories = data_handler.read_data('sample_data/answer.csv')
#     for item in stories:
#         if item["question_id"] == str(question_id):
#             result.append(item)
#
#     return render_template("answer.html", stories=result, question_id=question_id)
#
#
# @app.route("/answer_downvoting/<int:question_id>")
# def answerdownvoting(question_id=None):
#     story = {"id": "",
#              "submission_time": "",
#              "vote_number": "",
#              "question_id": "",
#              "message": "",
#              "image":  ""}
#
#     stories = data_handler.read_data('sample_data/answer.csv')
#     for item in stories:
#         if item["id"] == str(question_id):
#             story["vote_number"]=str(int(item["vote_number"])-1)
#             story["id"] = item["id"]
#             story["submission_time"] = item["submission_time"]
#             story["question_id"] = item["question_id"]
#             story["message"] = item["message"]
#             story["image"] = item["image"]
#
#     data_handler.write_data('sample_data/answer.csv', story)
#     result = []
#     stories = data_handler.read_data('sample_data/answer.csv')
#     for item in stories:
#         if item["question_id"] == str(question_id):
#             result.append(item)
#
#     return render_template("answer.html", stories=result, question_id=question_id)
