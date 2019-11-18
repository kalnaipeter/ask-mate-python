from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime
import time
import database_common

# @database_common.connection_handler
# def get_question_id(cursor):
#     cursor.execute("""
#                     SELECT question_id FROM answer;
#                     """)
#     question_id = cursor.fetchall()
#     return question_id


@database_common.connection_handler
def read_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question;
                   """)
    questions = cursor.fetchall()
    return questions

@database_common.connection_handler
def read_answers(cursor,question_id):
    cursor.execute("""
                        SELECT * FROM answer
                        WHERE question_id = %(question_id)s;
                       """,
                   {"question_id":question_id}
                   )
    stories= cursor.fetchall()
    return stories


@database_common.connection_handler
def write_question(cursor,submission_time,view_number,vote_number,title,message):
   cursor.execute("""
                INSERT INTO question (submission_time,view_number,vote_number,title,message)
                VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s);
                    """,
                   {"submission_time": submission_time,
                    "view_number": view_number,
                    "vote_number": vote_number,
                    "title": title,
                    "message": message}
                  )






@database_common.connection_handler
def write_answer(cursor,submission_time,vote_number,question_id,message):
   cursor.execute("""
                INSERT INTO answer (submission_time,vote_number,question_id,message)
                VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s);
                    """,

                   {"submission_time": submission_time,
                    "vote_number": vote_number,
                    "message": message,
                    "question_id":question_id})

@database_common.connection_handler
def get_question_data(cursor,question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s
                    """,
                   {"question_id":question_id})
    data = cursor.fetchall()
    print(data)
    return data
@database_common.connection_handler
def edit_question(cursor,question_id,title,message):
    cursor.execute("""
                    UPDATE question
                    SET title=%(title)s,message=%(message)s
                    WHERE id = %(question_id)s;
                    """,
                   {"title":title,
                    "message":message,
                    "question_id": question_id
                    })


def delete_question(question_file,question_id):
    stories = read_data(question_file)

    with open(question_file, "w") as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image'])
        writer.writeheader()

        for item in stories:
            if item["id"] != str(question_id):
                item["submission_time"] = \
                    str(int(time.mktime(datetime.strptime(item["submission_time"], '%Y-%m-%d %H:%M').timetuple())))
                writer.writerow(item)


def increase_view_number(question_file,question_id):
    questions = read_data(question_file)
    for question in questions:
        if question["id"] == str(question_id):
            story = question
            story["view_number"] = str(int(story["view_number"]) + 1)
    write_data(question_file, story)


def vote(start_file, target_file, question_id, vote_up,question):
    story = None

    stories = read_data(start_file)
    for item in stories:
        if item["id"] == str(question_id):
            story = item
            if not vote_up:
                story["vote_number"] = str(int(story["vote_number"]) - 1)
            else:
                story["vote_number"] = str(int(story["vote_number"]) + 1)

    write_data(start_file, story)
    stories = read_data(start_file)
    if not question:
        return get_question_id(start_file,"sample_data/question.csv",question_id,target_file)
    else:
        return render_template(target_file, stories=stories)
