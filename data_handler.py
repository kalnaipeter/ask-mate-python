import database_common
from datetime import datetime
import re

def get_the_current_date():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    return dt_string

@database_common.connection_handler
def sort_by_view(cursor):
    cursor.execute("""
                        SELECT * FROM question 
                        ORDER BY view_number DESC 
                        """)
    number = cursor.fetchall()
    return number

@database_common.connection_handler
def sort_by_vote(cursor):
    cursor.execute("""
                        SELECT * FROM question 
                        ORDER BY vote_number DESC 
                        """)
    voted = cursor.fetchall()
    return voted

@database_common.connection_handler
def sort_by_title(cursor):
    cursor.execute("""
                        SELECT * FROM question 
                        ORDER BY title ASC 
                        """)
    title = cursor.fetchall()
    return title

@database_common.connection_handler
def sort_by_message(cursor):
    cursor.execute("""
                        SELECT * FROM question 
                        ORDER BY message ASC 
                        """)
    message = cursor.fetchall()
    return message

def my_highlight_phrase():
    def _highlight_phrase(text_content, phrase):
        if phrase == None:
            return text_content
        pattern = re.compile(phrase, re.IGNORECASE)
        return pattern.sub(f'<span class="highlight">{phrase}</span>', text_content)
    return dict(highlight_phrase=_highlight_phrase)


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
def get_comment_message(cursor, comment_id):
    cursor.execute("""
                    SELECT message FROM comment
                    WHERE id = %(comment_id)s
                    """,
                   {"comment_id": comment_id})
    comment_message_dictionary = cursor.fetchone()
    return comment_message_dictionary["message"]

@database_common.connection_handler
def display_latest(cursor):
    cursor.execute("""
                    SELECT * FROM question 
                    ORDER BY submission_time DESC 
                    LIMIT 5
                    """)
    time = cursor.fetchall()
    return time


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
def get_question_id_from_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})

    question_dictionary = cursor.fetchone()
    return question_dictionary["question_id"]


@database_common.connection_handler
def get_question_id_from_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {"comment_id": comment_id})

    question_dictionary = cursor.fetchone()
    return question_dictionary["question_id"]


@database_common.connection_handler
def get_answer_id_from_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT answer_id FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {"comment_id": comment_id})

    answer_dictionary = cursor.fetchone()
    return answer_dictionary["answer_id"]


@database_common.connection_handler
def get_answer_ids_with_question_id(cursor,question_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {"question_id":question_id})
    answer_ids_dictionary = cursor.fetchall()
    return [item["id"] for item in answer_ids_dictionary]


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
def edit_comment(cursor, comment_id, message):
    cursor.execute("""
                    UPDATE comment
                    SET message=%(message)s
                    WHERE id = %(comment_id)s;
                    """,
                   {"message": message,
                    "comment_id": comment_id})


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
def write_question(cursor, submission_time, view_number, vote_number, title, message, image):
    cursor.execute("""
                    INSERT INTO question (submission_time,view_number,vote_number,title,message,image)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s);
                    """,
                   {"submission_time": submission_time,
                    "view_number": view_number,
                    "vote_number": vote_number,
                    "title": title,
                    "message": message,
                    "image":image})


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
    return data


@database_common.connection_handler
def get_search_result(cursor,item):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE title LIKE %(item)s OR message LIKE %(item)s;
                    """,
                   {"item":'%'+item+'%'} )
    resoult = cursor.fetchall()
    return resoult


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
                        DELETE FROM comment
                        WHERE question_id = %(question_id)s;
                        DELETE FROM answer
                        WHERE question_id = %(question_id)s;
                        DELETE FROM question
                        WHERE id = %(question_id)s;
                        """,
                   {"question_id": question_id})


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s;
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id":answer_id})

@database_common.connection_handler
def delete_comment(cursor,comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {"comment_id":comment_id})


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
