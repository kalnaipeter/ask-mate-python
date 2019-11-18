import database_common

@database_common.connection_handler
def read_questions(cursor):
    cursor.execute("""
                        SELECT * FROM question;
                       """
                   )
    stories= cursor.fetchall()

    return stories

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


def new_story(question_file, target_file, request_id, request_title, request_message,request_view_number,request_vote_number,request_image):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    story = {"id": request_id if request_id is not None else "",
             "submission_time": dt_string,
             "view_number": request_view_number,
             "vote_number": request_vote_number,
             "title": request_title,
             "message": request_message,
             "image": request_image
             }

    write_data(question_file, story)
    stories = read_data(question_file)
    return render_template(target_file, stories=stories)


def new_answer(answer_file, question_file, target_file, question_id, request_message):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M")

    story = {"id": "",
             "submission_time": dt_string,
             "vote_number": "",
             "question_id": question_id,
             "message": request_message,
             "image": ""
             }

    questions = read_data(question_file)
    question_title = None
    for item in questions:
        if item["id"] == str(question_id):
            question_title = item["title"]

    write_data(answer_file, story)
    result = []
    stories = read_data(answer_file)
    for item in stories:
        if item["question_id"] == str(question_id):
            result.append(item)

    return render_template(target_file, stories=result, question_id=question_id, question_title=question_title)


def get_answers(question_file, answer_file, target_file, question_id):
    questions = read_data(question_file)
    question_title = None
    for item in questions:
        if item["id"] == str(question_id):
            question_title = item["title"]
    story = None
    result = []
    stories = read_data(answer_file)
    for item in stories:
        if item["question_id"] == str(question_id):
            result.append(item)

    return render_template(target_file, stories=result, question_id=question_id,
                           question_title=question_title)


def get_question_id(answer_file,question_file,answer_id,target_file):
    answers = read_data(answer_file)
    question_id = None
    for answer in answers:
        if answer["id"] == str(answer_id):
            question_id = answer["question_id"]
    return get_answers(question_file,answer_file,target_file,question_id)



def edit_question(question_file, target_file, question_id):
    question_title = None
    question_message = None
    question_view_number = None
    question_vote_number = None
    question_image = None
    stories = read_data(question_file)
    for story in stories:
        if str(question_id) == story["id"]:
            question_title = story["title"]
            question_message = story["message"]
            question_view_number = story["view_number"]
            question_vote_number = story["vote_number"]
            question_image = story["image"]

    return render_template(target_file, question_image=question_image,question_vote_number=question_vote_number,
                           question_view_number=question_view_number,question_id=question_id, question_message=question_message,
                           question_title=question_title)


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
