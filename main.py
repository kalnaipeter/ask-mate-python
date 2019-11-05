from flask import Flask
import time

@app.route("/list")
def route_main():




app = Flask(__name__)

if __name__=="__main__":
    app.run(debug=True)