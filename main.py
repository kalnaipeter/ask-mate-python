from flask import Flask, render_template, request, redirect,url_for
from datetime import datetime
import data_handler

app = Flask(__name__)


@app.route('/')
def start():
    return redirect('/list')

@app.route("/question/search",methods=["POST"])
def search():
    search_result = request.form.get("search")
    print(search_result)
    story = data_handler.get_search_result(search_result)
    print(story)
    return render_template('search_resoult.html', stories=story)

@app.route('/list', methods=["GET", "POST"])
def route_list_questions():
    if request.method == "POST":
        time = data_handler.get_the_current_date()
        data_handler.write_question(time,0,0, request.form.get("title"), request.form.get("message"))
        stories = data_handler.read_questions()
        return render_template('questions.html', stories=stories)

    if request.method == "GET":
        stories = data_handler.read_questions()
        return render_template('questions.html', stories=stories)


@app.route('/question/<int:question_id>/edit',methods=["GET","POST"])
def route_edit_question(question_id):
    if request.method == "GET":
        question_title = data_handler.get_question_title(question_id)
        question_message = data_handler.get_question_message(question_id)
        return render_template("edit-question.html",question_title=question_title,question_message=question_message,question_id=question_id)
    if request.method == "POST":
        data_handler.edit_question(question_id,request.form.get("title"), request.form.get("message"))
        stories = data_handler.read_questions()
        return render_template('questions.html', stories=stories)


@app.route('/question/<int:question_id>/new-comment',methods=["GET","POST"])
def route_new_question_comment(question_id):
    if request.method == "GET":
        return render_template("add_new_question_comment.html", id=question_id)
    if request.method == "POST":
        time = data_handler.get_the_current_date()
        data_handler.write_question_comments(question_id,request.form.get("message"),time)
        return redirect(url_for("route_list_answers",question_id=question_id))


@app.route('/answer/<int:answer_id>/new-comment',methods=["GET","POST"])
def route_new_answer_comment(answer_id):
    if request.method == "GET":
        print("jeje")
        return render_template("add_new_answer_comment.html", id=answer_id)
    if request.method == "POST":
        time = data_handler.get_the_current_date()
        print(time)
        data_handler.write_answer_comments(answer_id, request.form.get("message"), time)
        question_id = data_handler.get_question_id(answer_id)
        print(question_id)
        return redirect(url_for("route_list_answers",question_id=question_id))


@app.route('/question/<int:question_id>/delete')
def route_delete_question(question_id):
    data_handler.delete_question(question_id)
    return redirect('/list')


@app.route('/add-question')
def route_add_new_question():
    return render_template("add-question.html")


@app.route('/answers/<int:question_id>', methods=["GET", "POST"])
def route_list_answers(question_id=None):
    if request.method == "GET":
        data_handler.increase_view_number(question_id)
        answers = data_handler.read_answers(question_id)
        question_comments = data_handler.read_question_comments(question_id)
        answer_comments = data_handler.read_comments()
        question_title = data_handler.get_question_title(question_id)
        return render_template("answer.html",question_title=question_title,question_id=question_id,answers=answers,
                               question_comments=question_comments,answer_comments=answer_comments)

    if request.method == "POST":
        time = data_handler.get_the_current_date()
        data_handler.write_answer(time,0,question_id,request.form.get("message"))
        answers = data_handler.read_answers(question_id)
        question_title = data_handler.get_question_title(question_id)
        return render_template("answer.html",question_title=question_title,answers=answers,question_id=question_id)


@app.route('/answers/<int:question_id>/add-new-answer')
def route_add_new_answer(question_id=None):
    return render_template("add-new-answer.html", question_id=question_id)


@app.route("/question/<int:question_id>/vote_up", methods=["POST"])
def question_vote_up(question_id=None):
    data_handler.question_vote_up(question_id)
    return redirect(url_for("route_list_questions"))


@app.route("/question/<int:question_id>/vote_down", methods=["POST"])
def question_vote_down(question_id=None):
    data_handler.question_vote_down(question_id)
    return redirect(url_for("route_list_questions"))


@app.route("/answer/<int:answer_id>/vote_up", methods=["POST"])
def answer_vote_up(answer_id=None):
    data_handler.answer_vote_up(answer_id)
    question_id = data_handler.get_question_id(answer_id)
    return redirect(url_for("route_list_answers",question_id=question_id))


@app.route("/answer/<int:answer_id>/vote_down", methods=["POST"])
def answer_vote_down(answer_id=None):
    data_handler.answer_vote_down(answer_id)
    question_id = data_handler.get_question_id(answer_id)
    return redirect(url_for("route_list_answers",question_id=question_id))


