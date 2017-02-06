import connections
import re
from flask import Flask, render_template, request
import time
import json

tt = time.localtime(time.time())

app = Flask(__name__)
c, conn = connections.connection()
halls = []


@app.route('/')
def hello_world():

    c.execute("SELECT hall_name FROM hall")
    cc = c.fetchall()
    hall_names = []
    for c1 in cc:
        hall_names.append(''.join(c1))
        print(''.join(c1))
    print(hall_names)
    global halls
    halls = hall_names
    return render_template('home.html', hall_names=halls)


class event:
    def __init__(self, name, location, time):
        self.name = name
        self.location = location
        self.time = time

ee_dict = {}


@app.route('/<hall_name>', methods=['GET', 'POST'])
def hall_lookup(hall_name):

    """
        The server gets updated at 7AM everyday. Cannot be done during night, as
        the UC website goes under maintenance from midnight to 6AM.
        Takes around 60 secs to get updated.
    """

    if tt.tm_hour == 7:

        import loadAll

    global halls
    hall_name = hall_name
    events = []
    print("hall_name = ")
    print(hall_name)
    if request.method == "GET":
        c.execute("SELECT event_name, location, event_time FROM events WHERE hall_name=(%s)", (hall_name,))
        events = c.fetchall()
    print(events[0])
    print(type(events))
    x = {"one": 1, "two": 2, "three": 3}
    print(x["one"])
    ee = {}
    for e in events:
        print("in for loop")
        ob = event(re.sub('[^A-Za-z ]+', '', e[0]), re.sub('[^A-Za-z0-9: ]+', '', e[1]), re.sub('[^A-Za-z0-9: ]+', '', e[2]))
        details = [ob.location, ob.time]
        print(details)
        ee[ob.name] = details
    print(ee)
    global ee_dict
    ee_dict = ee
    print(json.dumps(ee_dict))
    # return json.dumps(ee_dict)

    return render_template('home.html', events=ee, hall_names=halls, hall_name=hall_name)

'''
@app.route('/search/', methods=["GET", "POST"])
def search():
    searchfor = request.form['searchfor']
    print(searchfor)
    result = []
    print(ee_dict)
    for k in ee_dict:
        for v in ee_dict[k]:
            print(v)
            if searchfor in v:
                print(v)
                result.append(v)
    print(result)

    return
    #return render_template('home.html', hall_names=halls, search_results=result)
'''
if __name__ == '__main__':
    app.run()
