import csv
from datetime import datetime
import time


def read_data(file_name):
    stories = []

    with open(file_name) as file:
        lines = csv.DictReader(file)

        for line in lines:
            for key in line.keys():
                if key == "submission_time":
                    line[key] = datetime.fromtimestamp(int(line[key])).strftime('%Y-%m-%d %H:%M')
            story = dict(line)
            stories.append(story)

        return stories


def write_data(file_name, story):
    if file_name == "sample_data/answer.csv":
        fields = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

    elif file_name == "sample_data/question.csv":
        fields = ['id','submission_time','view_number','vote_number','title','message','image']

    stories = read_data(file_name)
    count = 0

    with open(file_name, "w") as file:
        writer = csv.DictWriter(file,fieldnames=fields)
        writer.writeheader()

        for item in stories:
            if 'id' in item:
                count += 1

        for item in stories:
            if item["id"] == str(story["id"]):
                item = story
            item["submission_time"] = str(int(time.mktime(datetime.strptime(item["submission_time"], '%Y-%m-%d %H:%M').timetuple())))
            writer.writerow(item)

        if story["id"] == "":
            story["submission_time"] = str(int(time.mktime(datetime.strptime(story["submission_time"], '%Y-%m-%d %H:%M').timetuple())))
            story['id'] = str(count)
            story['vote_number'] = "0"
            writer.writerow(story)
