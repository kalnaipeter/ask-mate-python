import database_common
from datetime import datetime
import re
import bcrypt


def get_hash_from_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    decoded_hash = hashed_password.decode('utf-8')
    return decoded_hash


def verify_password(password, hash):
    hashed_bytes_password = hash.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""
                    SELECT id FROM usertable
                    WHERE username = %(username)s
                    """,
                   {"username":username})
    id_dict = cursor.fetchone()
    return id_dict["id"]


@database_common.connection_handler
def get_usernames_from_database(cursor):
    cursor.execute("""
                    SELECT username FROM usertable
                    """,)
    names = cursor.fetchall()
    return [item["username"] for item in names]


@database_common.connection_handler
def get_user_id_with_question_id(cursor,question_id):
    cursor.execute("""
                    SELECT user_id FROM question
                    WHERE id = %(question_id)s
                    """,
                   {"question_id":question_id})
    user_id_dict = cursor.fetchone()
    return user_id_dict["user_id"]


@database_common.connection_handler
def get_username_of_a_question(cursor,user_id):
    cursor.execute("""
                    SELECT username FROM usertable
                        JOIN question
                        ON %(user_id)s = usertable.id
                    """,
                   {"user_id":user_id})
    username_dict = cursor.fetchone()
    return username_dict["username"]


@database_common.connection_handler
def get_username_of_a_comment(cursor,user_id):
    cursor.execute("""
                        SELECT username FROM usertable
                            JOIN comment
                            ON %(user_id)s = usertable.id
                        """,
                   {"user_id": user_id})
    username_dict = cursor.fetchone()
    return username_dict["username"]


@database_common.connection_handler
def get_username_of_an_answer(cursor,user_id):
    cursor.execute("""
                            SELECT username FROM usertable
                                JOIN answer
                                ON %(user_id)s = usertable.id
                            """,
                   {"user_id": user_id})
    username_dict = cursor.fetchone()
    return username_dict["username"]

@database_common.connection_handler
def get_hash_from_database(cursor,username):
    cursor.execute("""
                    SELECT password FROM usertable
                    WHERE username = %(username)s
                    """,
                   {"username":username})
    hash = cursor.fetchone()
    return hash


@database_common.connection_handler
def registration(cursor,username,password):
    hashed_bytes = get_hash_from_password(password)
    current_date = get_the_current_date()
    cursor.execute("""
                    INSERT INTO usertable (username,password,submission_time)
                    VALUES (%(username)s,%(hashed_bytes)s,%(current_date)s);
                   """,
                   {"username":username,
                    "hashed_bytes":hashed_bytes,
                    "current_date":current_date})

@database_common.connection_handler
def list_users(cursor,user):
    cursor.execute("""
                    SELECT username,submission_time
                    FROM usertable
                    WHERE username = 
                    """,)
    users = cursor.fetchall()
    return users



@database_common.connection_handler
def list_users(cursor):
    cursor.execute("""
                    SELECT username,submission_time
                    FROM usertable
                    """,)
    users = cursor.fetchall()
    return users


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
def get_answer_message(cursor,answer_id):
    cursor.execute("""
                    SELECT message FROM answer
                    WHERE id= %(answer_id)s
                    """,
                   {"answer_id":answer_id})
    answer_message_dictionary = cursor.fetchone()
    return answer_message_dictionary["message"]


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
                    ORDER BY submission_time DESC;
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
                   {"question_id": question_id})
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
def write_question_comments(cursor, question_id, message, submission_time,user_id):
    cursor.execute("""
                    INSERT INTO comment (question_id,message,submission_time,user_id)
                    VALUES (%(question_id)s,%(message)s,%(submission_time)s,%(user_id)s);
                    """,
                   {"question_id": question_id,
                    "message": message,
                    "submission_time": submission_time,
                    "user_id":user_id})


@database_common.connection_handler
def write_answer_comments(cursor, answer_id, message, submission_time,user_id):
    cursor.execute("""
                    INSERT INTO comment (answer_id,message,submission_time,user_id)
                    VALUES (%(answer_id)s,%(message)s,%(submission_time)s,%(user_id)s);
                    """,
                   {"answer_id": answer_id,
                    "message": message,
                    "submission_time": submission_time,
                    "user_id":user_id})


@database_common.connection_handler
def write_question(cursor, submission_time, view_number, vote_number, title, message, image,user_id):
    cursor.execute("""
                    INSERT INTO question (submission_time,view_number,vote_number,title,message,image,user_id)
                    VALUES (%(submission_time)s,%(view_number)s,%(vote_number)s,%(title)s,%(message)s,%(image)s,%(user_id)s);
                    """,
                   {"submission_time": submission_time,
                    "view_number": view_number,
                    "vote_number": vote_number,
                    "title": title,
                    "message": message,
                    "image":image,
                    "user_id":user_id})


@database_common.connection_handler
def write_answer(cursor, submission_time, vote_number, question_id, message,image,user_id):
    cursor.execute("""
                INSERT INTO answer (submission_time,vote_number,question_id,message,image,user_id)
                VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s,%(image)s,%(user_id)s);
                    """,

                   {"submission_time": submission_time,
                    "vote_number": vote_number,
                    "message": message,
                    "question_id": question_id,
                    "image":image,
                    "user_id":user_id})


@database_common.connection_handler
def get_image(cursor,question_id):
    cursor.execute("""
                    SELECT image FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {"question_id":question_id})
    image = cursor.fetchone()
    return image["image"]


@database_common.connection_handler
def get_answer_image(cursor,answer_id):
    cursor.execute("""
                    SELECT image FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id":answer_id})
    answer_image = cursor.fetchone()
    return answer_image["image"]


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
    print(item)

    cursor.execute("""
                    SELECT * FROM question
                    WHERE title LIKE %(item)s OR message LIKE %(item)s;
                    """,
                   {"item":'%'+item+'%'} )
    resoult = cursor.fetchall()
    return resoult


@database_common.connection_handler
def edit_question(cursor, question_id, title, message,image):
    cursor.execute("""
                    UPDATE question
                    SET title=%(title)s,message=%(message)s,image=%(image)s
                    WHERE id = %(question_id)s;
                    """,
                   {"title": title,
                    "message": message,
                    "question_id": question_id,
                    "image":image})


@database_common.connection_handler
def edit_answer(cursor, answer_id, message,image):
    cursor.execute("""
                    UPDATE answer
                    SET message=%(message)s,image=%(image)s
                    WHERE id = %(answer_id)s;
                    """,
                   {"message": message,
                    "answer_id": answer_id,
                    "image":image})


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
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number -1
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})
