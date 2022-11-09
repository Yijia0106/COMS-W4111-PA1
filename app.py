import os
from flask import Flask, request, render_template, g, redirect, Response
import db


app = Flask(__name__)
# engine = db.getEngine()

# data below is for test purpose and is related to result() func
max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine", "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
    {"name": "Fritz", "score": 40},
    {"name": "Sirius", "score": 75},
]


@app.route('/')
def index():
    return render_template("index.html", name="Yaochen Shen")


# test purpose function
@app.route("/results")
def result():
    context = {
        "title": "Results",
        "students": students,
        "test_name": test_name,
        "max_score": max_score,
    }
    return render_template("random/results.html", **context)


# @app.before_request
# def before_request():
#     try:
#         g.conn = engine.connect()
#     except:
#         print("uh oh, problem connecting to database")
#         g.conn = None
#
#
# @app.teardown_request
# def teardown_request(exception):
#     try:
#         g.conn.close()
#     except:
#         pass


if __name__ == "__main__":
    app.run(debug=True)
