from flask import Flask, render_template, request, redirect

import data_handler

app = Flask(__name__)


@app.route('/')
def start():
    return redirect('/list')


@app.route('/list')
def route_main():
    stories = data_handler.read_data('sample_data/question.csv')
    return render_template('list.html', stories=stories)


@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def route_question(question_id = None):
    if request.method == "GET":
        result = None
        stories = data_handler.read_data('sample_data/answer.csv')
        for item in stories:
            for value in item.values():
                if value == str(question_id):
                    result = item




if __name__ == "__main__":
    app.run(debug=True)
