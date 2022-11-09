import os
from flask import Flask, request, render_template, g, redirect, Response
import db

app = Flask(__name__)
engine = db.getEngine()

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


@app.route('/submitAvailabilityRequestByName', methods=['POST'])
def submitAvailabilityRequestByName():
    name = request.form.get('byName')
    return str(name)


@app.route('/submitAvailabilityRequestByDate', methods=['POST'])
def submitAvailabilityRequestByDate():
    if request.method == "POST":
        from_date = request.form.get('fromDate')
        to_date = request.form.get('toDate')
        return f'{from_date} should be earlier than {to_date}'


@app.route('/allShows', methods=['GET'])
def allShows():
    cursor = g.conn.execute("SELECT * FROM shows")
    shows = []
    for entry in cursor:
        show = dict()
        show['name'] = entry[1]
        show['description'] = entry[2]
        shows.append(show)

    cursor.close()
    context = dict(shows=shows)
    return render_template("all-shows-info/showInfoResults.html", **context)


# @app.route('/prevOrders', methods=['GET'])
# def prevOrders():


# test purpose function
@app.route('/database')
def db():
    cursor = g.conn.execute("SELECT * FROM customers")
    users = []
    for entry in cursor:
        user = dict()
        user['name'] = entry[1]
        user['email'] = entry[2]
        user['number'] = entry[3]
        users.append(user)
    cursor.close()
    context = dict(users=users)
    return render_template("random/users.html", **context)


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


@app.before_request
def before_request():
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        g.conn = None


@app.teardown_request
def teardown_request(exception):
    try:
        g.conn.close()
    except:
        pass


#
# if __name__ == "__main__":
#     app.run(debug=True, port=8111)

if __name__ == "__main__":
    import click


    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()
