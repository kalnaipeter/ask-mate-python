from flask import Flask, render_template, request, redirect
from datetime import datetime
import data_handler

app = Flask(__name__)


@app.route('/')
def start():
    return redirect('/list')


@app.route('/list', methods=["GET", "POST"])
def route_list_questions():
    if request.method == "POST":
        return data_handler.new_story('sample_data/question.csv', 'questions.html',
                                      request.form.get("question_id"), request.form.get("title"),
                                      request.form.get("message"),request.form.get("view_number"),
                                      request.form.get("vote_number"),request.form.get("image"))
    if request.method == "GET":
        stories = data_handler.read_data('sample_data/question.csv')
        return render_template('questions.html', stories=stories)


@app.route('/question/<int:question_id>/edit')
def route_edit_question(question_id):
    return data_handler.edit_question("sample_data/question.csv", "add-question.html", question_id)


@app.route('/question/<int:question_id>/delete')
def route_delete_question(question_id):
    data_handler.delete_question("sample_data/question.csv",question_id)
    return redirect('/list')


@app.route('/add-question')
def route_add_new_question():
    return render_template("add-question.html")


@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def route_list_answers(question_id=None):
    if request.method == "GET":
        data_handler.increase_view_number('sample_data/question.csv',question_id)
        return data_handler.get_answers('sample_data/question.csv', 'sample_data/answer.csv', "answer.html",
                                        question_id)

    if request.method == "POST":
        return data_handler.new_answer('sample_data/answer.csv', 'sample_data/question.csv',
                                       "answer.html", question_id, request.form.get("message"))


@app.route('/question/<int:question_id>/add-new-answer')
def route_add_new_answer(question_id=None):
    return render_template("add-new-answer.html", question_id=question_id)


@app.route("/question/<int:question_id>/vote_up", methods=["POST"])
def question_vote_up(question_id=None):
    return data_handler.vote("sample_data/question.csv", 'questions.html', question_id, True,True)


@app.route("/question/<int:question_id>/vote_down", methods=["POST"])
def question_vote_down(question_id=None):
    return data_handler.vote("sample_data/question.csv",'questions.html',question_id,False,True)


@app.route("/answer/<int:answer_id>/vote_up", methods=["POST"])
def answer_vote_up(answer_id=None):
    return data_handler.vote("sample_data/answer.csv", 'answer.html', answer_id, True,False)


@app.route("/answer/<int:answer_id>/vote_down", methods=["POST"])
def answer_vote_down(answer_id=None):
    return data_handler.vote("sample_data/answer.csv", 'answer.html', answer_id, False,False)


