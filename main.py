from flask import Flask, render_template, request, redirect,url_for
from datetime import datetime
import data_handler
import re

import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





@app.route('/')
def start():
    return redirect('/list')


@app.route('/list', methods=["GET", "POST"])
def route_list_questions():
    if request.method == "POST":
        time = data_handler.get_the_current_date()
        if request.files['file']:
            file = request.files['file']
            file.save("/home/korsos/PycharmProjects/askme/ask-mate-python/static/images/" + file.filename)
            data_handler.write_question(time,0,0, request.form.get("title"), request.form.get("message"),file.filename)
        else:
            data_handler.write_question(time, 0, 0, request.form.get("title"), request.form.get("message"),None)
        stories = data_handler.read_questions()
        return render_template('questions.html', stories=stories, fancy_word=None)

    if request.method == "GET":
        stories = data_handler.read_questions()
        return render_template('questions.html', stories=stories,fancy_word=None)


@app.route('/question/<int:question_id>/edit',methods=["GET","POST"])
def route_edit_question(question_id):
    if request.method == "GET":
        question_title = data_handler.get_question_title(question_id)
        question_message = data_handler.get_question_message(question_id)
        return render_template("edit-question.html",question_title=question_title,question_message=question_message,question_id=question_id)
    if request.method == "POST":
        data_handler.edit_question(question_id,request.form.get("title"), request.form.get("message"))
        stories = data_handler.read_questions()
        return render_template('questions.html', stories=stories,fancy_word=None)


@app.route('/question/<int:question_id>/delete')
def route_delete_question(question_id):
    for item in data_handler.get_answer_ids_with_question_id(question_id):
        data_handler.delete_answer(item)
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


@app.route('/answer/<int:answer_id>/delete')
def route_delete_answer(answer_id):
    question_id = data_handler.get_question_id_from_answer_id(answer_id)
    data_handler.delete_answer(answer_id)
    return redirect(url_for("route_list_answers",question_id=question_id))


@app.route('/comment/<int:comment_id>/delete')
def route_delete_comment(comment_id):
    question_id = data_handler.get_question_id_from_comment_id(comment_id)
    if question_id is None:
        answer_id = data_handler.get_answer_id_from_comment_id(comment_id)
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
    data_handler.delete_comment(comment_id)
    return redirect(url_for("route_list_answers", question_id=question_id))


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
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return render_template("add_new_answer_comment.html", id=answer_id,question_id=question_id)
    if request.method == "POST":
        time = data_handler.get_the_current_date()
        data_handler.write_answer_comments(answer_id, request.form.get("message"), time)
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return redirect(url_for("route_list_answers",question_id=question_id))


@app.route('/comment/<int:comment_id>/edit', methods=["GET", "POST"])
def route_edit_comment(comment_id=None):
    if request.method == "GET":
        comment_message = data_handler.get_comment_message(comment_id)
        question_id = data_handler.get_question_id_from_comment_id(comment_id)
        if question_id is None:
            answer_id = data_handler.get_answer_id_from_comment_id(comment_id)
            question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return render_template("edit-comment.html", comment_id=comment_id,comment_message=comment_message,question_id=question_id)
    if request.method == "POST":
        data_handler.edit_comment(comment_id,request.form.get("message"))
        question_id = data_handler.get_question_id_from_comment_id(comment_id)
        if question_id is None:
            answer_id = data_handler.get_answer_id_from_comment_id(comment_id)
            question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return redirect(url_for("route_list_answers", question_id=question_id))


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
    question_id = data_handler.get_question_id_from_answer_id(answer_id)
    return redirect(url_for("route_list_answers",question_id=question_id))


@app.route("/answer/<int:answer_id>/vote_down", methods=["POST"])
def answer_vote_down(answer_id=None):
    data_handler.answer_vote_down(answer_id)
    question_id = data_handler.get_question_id_from_answer_id(answer_id)
    return redirect(url_for("route_list_answers",question_id=question_id))



@app.route("/question/search",methods=["POST"])
def search():
    search_result = request.form.get("search")
    fancy_word = request.form.get("search")
    story = data_handler.get_search_result(search_result)

    return render_template('questions.html', stories=story, fancy_word=fancy_word)

@app.context_processor
def highlight_phrase():
    return data_handler.my_highlight_phrase()


@app.route('/question/order_by_time')
def latest_time():
    story = data_handler.display_latest()
    return render_template('questions.html', stories=story, fancy_word=None)

@app.route('/question/order_by_view')
def sort_by_view():
    story = data_handler.sort_by_view()
    return render_template('questions.html', stories=story, fancy_word=None)

@app.route('/question/order_by_vote')
def sort_by_vote():
    story = data_handler.sort_by_vote()
    return render_template('questions.html', stories=story, fancy_word=None)

@app.route('/question/order_by_title')
def sort_by_title():
    story = data_handler.sort_by_title()
    return render_template('questions.html', stories=story, fancy_word=None)

@app.route('/question/order_by_message')
def sort_by_message():
    story = data_handler.sort_by_message()
    return render_template('questions.html', stories=story, fancy_word=None)