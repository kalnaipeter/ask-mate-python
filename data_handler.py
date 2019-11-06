import csv
from datetime import datetime

def read_data(file_name):
    stories = []

    with open(file_name) as file:
        lines = csv.DictReader(file)

        for line in lines:
            for key in line.keys():
                if key == "submission_time":
                    line[key] = datetime.fromtimestamp(int(line[key])).strftime('%Y-%m-%d %H:%M:%S')
            story = dict(line)
            stories.append(story)



        return stories


