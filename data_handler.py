from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
import time
import database_common
import psycopg2


def get_the_current_date():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string


@database_common.connection_handler
def get_question_message(cursor, question_id):
    cursor.execute("""
                    SELECT message FROM question
                    WHERE id= %(question_id)s
                    """,
                   {"question_id": question_id})
    question_message_dictionary = cursor.fetchone()
    return question_message_dictionary["message"]


@database_common.connection_handler
def get_question_title(cursor, question_id):
    cursor.execute("""
                    SELECT title FROM question
                    WHERE id= %(question_id)s
                    """,
                   {"question_id": question_id})
    question_title_dictionary = cursor.fetchone()
    return question_title_dictionary["title"]


@database_common.connection_handler
def get_question_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})

    question_dictionary = cursor.fetchone()
    return question_dictionary["question_id"]


@database_common.connection_handler
def read_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id;
                   """)
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def read_answers(cursor, question_id):
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id = %(question_id)s
                        ORDER BY id;
                       """,
                   {"question_id": question_id}
                   )
    stories = cursor.fetchall()
    return stories


@database_common.connection_handler
def read_question_comments(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s
                    """,
                   {"question_id": question_id})
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def read_comments(cursor):
    cursor.execute("""
                    SELECT * FROM comment;
                    """,)
    comments = cursor.fetchall()
    return comments


@database_common.connection_handler
def write_question_comments(cursor, question_id, message, submission_time):
    cursor.execute("""
                    INSERT INTO comment (question_id,message,submission_time)
                    VALUES (%(question_id)s,%(message)s,%(submission_time)s);
                    """,
                   {"question_id": question_id,
                    "message": message,
                    "submission_time": submission_time})


@database_common.connection_handler
def write_answer_comments(cursor, answer_id, message, submission_time):
    cursor.execute("""
                    INSERT INTO comment (answer_id,message,submission_time)
                    VALUES (%(answer_id)s,%(message)s,%(submission_time)s);
                    """,
                   {"answer_id": answer_id,
                    "message": message,
                    "submission_time": submission_time})


@database_common.connection_handler
def write_question(cursor, submission_time, view_number, vote_number, title, message):
    cursor.execute("""
                    INSERT INTO question (submission_time,view_number,vote_number,title,message)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s);
                    """,
                   {"submission_time": submission_time,
                    "view_number": view_number,
                    "vote_number": vote_number,
                    "title": title,
                    "message": message})


@database_common.connection_handler
def write_answer(cursor, submission_time, vote_number, question_id, message):
    cursor.execute("""
                INSERT INTO answer (submission_time,vote_number,question_id,message)
                VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s);
                    """,

                   {"submission_time": submission_time,
                    "vote_number": vote_number,
                    "message": message,
                    "question_id": question_id})


@database_common.connection_handler
def get_question_data(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s
                    """,
                   {"question_id": question_id})
    data = cursor.fetchall()
    print(data)
    return data


@database_common.connection_handler
def edit_question(cursor, question_id, title, message):
    cursor.execute("""
                    UPDATE question
                    SET title=%(title)s,message=%(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {"title": title,
                    "message": message,
                    "question_id": question_id})


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                        DELETE FROM answer
                        WHERE question_id = %(question_id)s;
                        DELETE FROM question
                        WHERE id = %(question_id)s;
                        """,
                   {"question_id": question_id})


@database_common.connection_handler
def increase_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(question_id)s;
                    """,
                   {"question_id": question_id})


@database_common.connection_handler
def question_vote_up(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number +1
                    WHERE id = %(question_id)s;
                    """,
                   {"question_id": question_id})


@database_common.connection_handler
def question_vote_down(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number -1
                    WHERE id = %(question_id)s;
                    """,
                   {"question_id": question_id})


@database_common.connection_handler
def answer_vote_up(cursor, answer_id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number +1
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})


@database_common.connection_handler
def answer_vote_down(cursor, answer_id):
    print(answer_id)
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number -1
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})
