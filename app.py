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

# yaoyao
@app.route('/')
def index():
    return render_template("index.html", name="Yaochen Shen")


@app.route('/submitAvailabilityRequestByName', methods=['POST'])
def submitAvailabilityRequestByName():
    name = request.form.get('byName')
    cursor = g.conn.execute("SELECT name, row, seat, section, theatre_name as Theatre, cdate as Date, ctime as Time, price FROM (AvailableOn a inner join Calendars cal ON a.cid = cal.cid) temp1 inner join (Select location_id, theatre_name, l.row_id as row, l.seat_id as seat, l.section, name From Locations l Left join (SELECT * FROM shows WHERE name ='{name1}') s on l.sid = s.sid) temp2 ON temp1.location_id = temp2.location_id WHERE order_number is Null and temp2.name ='{name1}'".format(name1=name))
    shows = []
    for entry in cursor:
        print(entry)

        show = dict()
        show['name'] = entry[0]
        show['row'] = entry[1]
        show['seat'] = entry[2]
        show['section'] = entry[3]
        show['theatre'] = entry[4]
        show['date'] = entry[5]
        show['time'] = entry[6]
        show['price'] = entry[7]
        shows.append(show)

    cursor.close()
    context = dict(shows=shows)
    return render_template("find-tickets-process/availability.html", **context)
    # return str(shows)


@app.route('/submitAvailabilityRequestByDate', methods=['POST'])
def submitAvailabilityRequestByDate():
    if request.method == "POST":
        from_date = request.form.get('fromDate')
        to_date = request.form.get('toDate')
        shows = []
        cursor = g.conn.execute("Select name as Show, row, seat, section, theatre_name as Theatre, cdate as Date, ctime as Time, price,  temp1.location_id, temp2.sid, temp1.ccid From (AvailableOn a inner join (Select cid as ccid, cdate, ctime From Calendars c Where c.cdate between CAST('{from_date}' AS DATE) and CAST('{to_date}' AS DATE)) cal on a.cid = cal.ccid) temp1 Left join (Select location_id, theatre_name, l.row_id as row, l.seat_id as seat, l.section, name, s.sid From Locations l Left join Shows s on l.sid = s.sid) temp2 on temp1.location_id = temp2.location_id Where order_number is Null".format(from_date=from_date, to_date=to_date))
        for entry in cursor:
            print(entry)

            show = dict()
            show['name'] = entry[0]
            show['row'] = entry[1]
            show['seat'] = entry[2]
            show['section'] = entry[3]
            show['theatre'] = entry[4]
            show['date'] = entry[5]
            show['time'] = entry[6]
            show['price'] = entry[7]

            show['id'] = str(entry[8]) + "," + str(entry[9]) + "," + str(entry[10])

            shows.append(show)

        cursor.close()
        context = dict(shows=shows)
        return render_template("find-tickets-process/availability.html", **context)
        # return f'{from_date} should be earlier than {to_date}'

@app.route('/fillPaymentInfo', methods=['POST'])
def fillPaymentInfo():
    chkbox_values = request.form.getlist('chkbox')
    c_name = request.form.get('cName')
    c_email = request.form.get('cEmail')
    c_phone = request.form.get('cPhone')

    print(c_name)
    print(c_email)
    print(c_phone)
    # g.conn.execute("INSERT INTO test(name) VALUES (:c_name), (:c_email), (:c_phone)", name1=name, name2=name);
    context = dict(shows=chkbox_values)
    return render_template("find-tickets-process/paymentInfo.html", **context)
    # return "HI"

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
        app.run(host=HOST, port=PORT, debug=True, threaded=threaded)


    run()
