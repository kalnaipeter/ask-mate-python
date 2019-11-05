import csv

def read_data(file_name):
    stories = []

    with open(file_name) as file:
        lines = csv.DictReader(file)

        for line in lines:
            story = dict(line)
            stories.append(story)

    return stories

