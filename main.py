from flask import Flask, render_template, request, redirect, url_for,make_response,session
from datetime import datetime
import data_handler
import re
import os

app = Flask(__name__)
path = os.path.dirname(__file__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/user_page')
def show_user_page():
    username = session["username"]
    user_id = data_handler.get_user_id(session["username"])
    user_questions = data_handler.get_user_questions(user_id)
    user_answers = data_handler.get_user_answers(user_id)
    user_data=data_handler.get_user_data(user_id)
    answer_comments = data_handler.read_comments()
    return render_template('user_page.html', user_data=user_data, username=username, user_questions=user_questions,answer_comments=answer_comments, user_answers=user_answers,fancy_word=None)


@app.route('/set-cookie')
def cookie_insertion():
    redirect_to_index = redirect('/')
    response = make_response(redirect_to_index)
    response.set_cookie('cookie-name', value='values')
    return response


@app.route('/')
def start():
    return render_template("login_and_registration.html")


@app.route('/registration',methods=["GET","POST"])
def registration():
    if request.method == "POST":
        if " " not in request.form["username"] and " " not in request.form["password"] \
                and request.form["username"] is not "" and request.form["password"] is not "":
            if request.form["username"] in data_handler.get_usernames_from_database():
                error = "This username is already in use"
                return render_template("login_and_registration.html", error=error)
            data_handler.registration(request.form["username"], request.form["password"], 0)
            return render_template("login_and_registration.html")
        error = "Wrong characters..."
        return render_template("login_and_registration.html", error=error)


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        if data_handler.get_hash_from_database(request.form["username"]) is not None:
            database_password = data_handler.get_hash_from_database(request.form["username"])
            verify_password = data_handler.verify_password(request.form["password"],database_password["password"])
            if verify_password:
                session["username"] = request.form["username"]
                return redirect(url_for("route_list_questions"))
        error = "Invalid username or password"
        return render_template("login_and_registration.html", error=error)
    return render_template("login_and_registration.html")


@app.route('/list_users')
def list_users():
    username = session["username"]
    users = data_handler.list_users()
    return render_template("list_users.html",users=users,username=username)


@app.route('/list', methods=["GET", "POST"])
def route_list_questions():
    if request.method == "POST":
        username = session["username"]
        user_id = data_handler.get_user_id(session["username"])
        time = data_handler.get_the_current_date()
        if request.files['file']:
            file = request.files['file']
            file.save(path + "/static/images/" + file.filename)
            data_handler.write_question(time, 0, 0, request.form.get("title"), request.form.get("message"),
                                        file.filename,user_id)
        else:
            data_handler.write_question(time, 0, 0, request.form.get("title"), request.form.get("message"), None,user_id)
        stories = data_handler.read_questions()
        return render_template('questions.html', username=username,stories=stories, fancy_word=None)
    if request.method == "GET":
        username = session["username"]
        column = "submission_time"
        direction = "DESC"
        opportunities = ["submission_time","vote_number","view_number","title","message"]
        if request.args.get("order_by") in opportunities:
            column = request.args.get("order_by")
        if request.args.get("direction") in opportunities:
            direction = request.args.get("direction")
        stories = data_handler.read_questions(column,direction)
        return render_template('questions.html', username=username,stories=stories, fancy_word=None)


@app.route('/question/<int:question_id>/edit', methods=["GET", "POST"])
def route_edit_question(question_id):
    if request.method == "GET":
        username = session["username"]
        question_title = data_handler.get_question_title(question_id)
        question_message = data_handler.get_question_message(question_id)
        return render_template("edit-question.html", question_title=question_title, question_message=question_message,
                               question_id=question_id,username=username)
    if request.method == "POST":
        if request.files['file']:
            file = request.files['file']
            file.save(path + "/static/images/" + file.filename)
            data_handler.edit_question(question_id, request.form.get("title"), request.form.get("message"),
                                       file.filename)
        else:
            data_handler.edit_question(question_id, request.form.get("title"), request.form.get("message"),
                                       data_handler.get_image(question_id))
        return redirect('/list')


@app.route('/question/<int:question_id>/delete')
def route_delete_question(question_id):
    for item in data_handler.get_answer_ids_with_question_id(question_id):
        data_handler.delete_answer(item)
    data_handler.delete_question(question_id)
    return redirect('/list')


@app.route('/add-question')
def route_add_new_question():
    username = session["username"]
    return render_template("add-question.html",username=username)


@app.route('/answers/<int:question_id>', methods=["GET", "POST"])
def route_list_answers(question_id=None):
    if request.method == "GET":
        data_handler.increase_view_number(question_id)
        answers = data_handler.read_answers(question_id)
        question_comments = data_handler.read_question_comments(question_id)
        answer_comments = data_handler.read_comments()
        question_title = data_handler.get_question_title(question_id)
        image = data_handler.get_image(question_id)
        user_id = data_handler.get_user_id_with_question_id(question_id)
        question_user_name = data_handler.get_username_of_a_question(user_id)
        username = session["username"]
        return render_template("answer.html",username=username,image=image, question_user_name=question_user_name,
                               question_title=question_title,question_id=question_id,answers=answers,
                               question_comments=question_comments,
                               answer_comments=answer_comments)
    if request.method == "POST":
        user_id = data_handler.get_user_id(session["username"])
        time = data_handler.get_the_current_date()
        if request.files['file']:
            file = request.files['file']
            file.save(path + "/static/images/" + file.filename)
            data_handler.write_answer(time, 0, question_id, request.form.get("message"), file.filename,user_id)
        data_handler.write_answer(time, 0, question_id, request.form.get("message"), None,user_id)
        return redirect(url_for("route_list_answers", question_id=question_id))


@app.route('/answer/<int:answer_id>/edit', methods=["GET", "POST"])
def route_edit_answer(answer_id):
    if request.method == "GET":
        answer_message = data_handler.get_answer_message(answer_id)
        username = session["username"]
        return render_template("edit_answer.html", answer_message=answer_message, answer_id=answer_id,username=username)
    if request.method == "POST":
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
        if request.files['file']:
            file = request.files['file']
            file.save(path + "/static/images/" + file.filename)
            data_handler.edit_answer(answer_id, request.form.get("message"), file.filename)
        else:
            data_handler.edit_answer(answer_id, request.form.get("message"), data_handler.get_answer_image(answer_id))
        return redirect(url_for("route_list_answers", question_id=question_id))


@app.route('/answers/<int:question_id>/add-new-answer')
def route_add_new_answer(question_id=None):
    username = session["username"]
    return render_template("add-new-answer.html", question_id=question_id, username=username)


@app.route('/answer/<int:answer_id>/delete')
def route_delete_answer(answer_id):
    question_id = data_handler.get_question_id_from_answer_id(answer_id)
    data_handler.delete_answer(answer_id)
    return redirect(url_for("route_list_answers", question_id=question_id))


@app.route('/comment/<int:comment_id>/delete')
def route_delete_comment(comment_id):
    question_id = data_handler.get_question_id_from_comment_id(comment_id)
    if question_id is None:
        answer_id = data_handler.get_answer_id_from_comment_id(comment_id)
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
    data_handler.delete_comment(comment_id)
    return redirect(url_for("route_list_answers", question_id=question_id))


@app.route('/question/<int:question_id>/new-comment', methods=["GET", "POST"])
def route_new_question_comment(question_id):
    if request.method == "GET":
        username = session["username"]
        return render_template("add_new_question_comment.html", id=question_id,username=username)
    if request.method == "POST":
        user_id = data_handler.get_user_id(session["username"])
        time = data_handler.get_the_current_date()
        data_handler.write_question_comments(question_id, request.form.get("message"), time,user_id)
        return redirect(url_for("route_list_answers", question_id=question_id))


@app.route('/answer/<int:answer_id>/new-comment', methods=["GET", "POST"])
def route_new_answer_comment(answer_id):
    if request.method == "GET":
        username = session["username"]
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return render_template("add_new_answer_comment.html", id=answer_id, question_id=question_id,username=username)
    if request.method == "POST":
        user_id = data_handler.get_user_id(session["username"])
        time = data_handler.get_the_current_date()
        data_handler.write_answer_comments(answer_id, request.form.get("message"), time,user_id)
        question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return redirect(url_for("route_list_answers", question_id=question_id))


@app.route('/comment/<int:comment_id>/edit', methods=["GET", "POST"])
def route_edit_comment(comment_id=None):
    if request.method == "GET":
        username = session["username"]
        comment_message = data_handler.get_comment_message(comment_id)
        # question_id = data_handler.get_question_id_from_comment_id(comment_id)
        if question_id is None:
            answer_id = data_handler.get_answer_id_from_comment_id(comment_id)
            # question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return render_template("edit-comment.html", comment_id=comment_id, comment_message=comment_message,username=username)
    if request.method == "POST":
        data_handler.edit_comment(comment_id, request.form.get("message"))
        question_id = data_handler.get_question_id_from_comment_id(comment_id)
        if question_id is None:
            answer_id = data_handler.get_answer_id_from_comment_id(comment_id)
            question_id = data_handler.get_question_id_from_answer_id(answer_id)
        return redirect(url_for("route_list_answers", question_id=question_id))


@app.route("/question/vote_up", methods=["POST"])
def question_vote(question_id=None,answer_id=None,vote=None):
    column = "submission_time"
    direction = "DESC"
    print(question_id)
    if question_id:
        print("ideis")
        user_id = data_handler.get_user_id_with_question_id(question_id)
        data_handler.question_reputaion_up(user_id)
        if vote == "up":
            data_handler.question_vote_up(question_id)
        data_handler.question_vote_down(question_id)
        print("ittleszabaj")
        return redirect(url_for("route_list_questions"))
    if answer_id:
        user_id = data_handler.get_user_id_by_answer_id(answer_id)
        data_handler.answer_reputaion_up(user_id)
        data_handler.answer_vote_up(answer_id)
        if vote == "up":
            data_handler.answer_vote_up(answer_id)
        data_handler.answer_vote_down(answer_id)
        return redirect(url_for("route_list_answers", question_id=question_id))



# @app.route("/question/<int:question_id>/vote_up", methods=["POST"])
# def question_vote_up(question_id=None):
#     user_id = data_handler.get_user_id_with_question_id(question_id)
#     data_handler.question_reputaion_up(user_id)
#     data_handler.question_vote_up(question_id)
#     return redirect(url_for("route_list_questions",))
#
#
# @app.route("/question/<int:question_id>/vote_down", methods=["POST"])
# def question_vote_down(question_id=None):
#     user_id = data_handler.get_user_id_with_question_id(question_id)
#     data_handler.question_reputaion_down(user_id)
#     data_handler.question_vote_down(question_id)
#     return redirect(url_for("route_list_questions"))
#
#
# @app.route("/answer/<int:answer_id>/vote_up", methods=["POST"])
# def answer_vote_up(answer_id=None):
#     user_id = data_handler.get_user_id_by_answer_id(answer_id)
#     data_handler.answer_reputaion_up(user_id)
#     data_handler.answer_vote_up(answer_id)
#     question_id = data_handler.get_question_id_from_answer_id(answer_id)
#     return redirect(url_for("route_list_answers", question_id=question_id))
#
#
# @app.route("/answer/<int:answer_id>/vote_down", methods=["POST"])
# def answer_vote_down(answer_id=None):
#     user_id = data_handler.get_user_id_by_answer_id(answer_id)
#     data_handler.answer_reputaion_down(user_id)
#     data_handler.answer_vote_down(answer_id)
#     question_id = data_handler.get_question_id_from_answer_id(answer_id)
#     return redirect(url_for("route_list_answers", question_id=question_id))


@app.route("/question/search", methods=["POST"])
def search():
    search_result = request.form.get("search")
    fancy_word = request.form.get("search")
    story = data_handler.get_search_result(search_result)

    return render_template('questions.html',username = session["username"],stories=story, fancy_word=fancy_word)


@app.context_processor
def highlight_phrase():
    return data_handler.my_highlight_phrase()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
