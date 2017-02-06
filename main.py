"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, render_template, request, redirect, session, url_for
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from google.appengine.api import memcache
import connections

import re
import time
import json


default_user = 'default_user'
app.config['SECRET_KEY'] = 'Suraj'
c, conn = connections.connection()

tt = time.localtime(time.time())
halls = []

if tt.tm_hour == 7:

        import loadAll

'''
def user_key(email=default_user):
    return ndb.Key('user', email)


class Users(ndb.Model):
    name = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=False)
    city = ndb.StringProperty(indexed=True)
    state = ndb.StringProperty(indexed=True)
    country = ndb.StringProperty(indexed=True)
'''


@app.route('/', methods=['POST', 'GET'])
def home():
    if "logged_in" not in session:
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            password = request.form['password1']
            repassword = request.form['password2']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            c.execute("SELECT email from user where email=(%s)", (email,))
            # query = Users.query(Users.email == email.capitalize())
            # user= query.fetch()
            user = c.fetchall()
            if len(user) == 0:
                if password == repassword:
                    # c.execute("insert into user (email) values (%s)", (email,))
                    # register = Users()
                    # register.email = email.capitalize()

                    if name.find(" ") != -1:
                        name1 = name.split(" ")
                        firstname = name1[0].capitalize()
                        lastname = name1[1].capitalize()
                        name = firstname + " " + lastname
                        # c.execute("insert into user (name) values (%s)", (firstname + " " + lastname, ))
                        # register.name = firstname + " " + lastname

                        # register.name = name
                        # c.execute("insert into user (name) values (%s)", (name, ))

                    '''
                    register.password = password
                    register.city = city.capitalize()
                    register.state = state.capitalize()
                    register.country = country.capitalize()
                    register.put()
                    '''
                    c.execute("insert into user (email, name, password, city, state, country) values "
                              "(%s, %s, %s, %s, %s, %s)", (email, name, password, city, state, country))
                    session['logged_in'] = name
                    conn.commit()
                    return render_template('events.html', hall_names=halls, name=name)
                else:
                    return render_template('home.html', error="Passwords must match")
            else:
                return render_template('home.html', error="Email already registered")
    else:
        return render_template('home1.html', name=session['logged_in'])

    return render_template('home.html')


@app.route('/log_out/', methods=['POST', 'GET'])
def log_out():
    if 'logged_in' in session:
        session.clear()
        return redirect(url_for('home'))
    else:
        return "Unauthorized Access"


@app.route('/signin/', methods=['POST', 'GET'])
def signin():
    email = request.form['emailsignin']
    password = request.form['passwordsignin']
    # query = Users.query(Users.email == email.capitalize())
    # user = query.fetch()
    c.execute("select email, password, name from user where email=(%s)", (email.capitalize(), ))
    user = c.fetchall()
    if len(user) == 1:
        if user[0][1] == password:
            session['logged_in'] = user[0][0]
            conn.commit()
            c.execute("SELECT hall_name FROM hall")
            cc = c.fetchall()
            hall_names = []
            for c1 in cc:
                hall_names.append(''.join(c1))
                print(''.join(c1))
            print(hall_names)
            global halls
            halls = hall_names
            return render_template('events.html', hall_names=halls)
        else:
            return render_template('home.html', error="Invalid email/password combination")
    return render_template('home.html', error="User does not exists")

'''
@app.route('/search/', methods=['POST', 'GET'])
def search():
    search = request.form['search'].capitalize()
    query = Users.query()

    users = query.fetch()
    users1 = memcache.get(search)
    if users1 is None:
        users1 = []
        for user in users:
            if user.name.find(search) != -1 and user not in users1:
                users1.append(user)
            if user.city.find(search) != -1 and user not in users1:
                users1.append(user)
            if user.state.find(search) != -1 and user not in users1:
                users1.append(user)
            if user.country.find(search) != -1 and user not in users1:
                users1.append(user)
            if user.email.find(search) != -1 and user not in users1:
                users1.append(user)
        memcache.add(search, users1)
    stats = memcache.get_stats()

    hits = stats['hits']
    misses = stats['misses']
    return render_template('home.html', users=users1, hits=hits, misses=misses)
'''

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

'''
<!--
<div style="width: 300px; float: right; margin: -60px 50px 0 0"><form method="post" action="{{ url_for('search') }}">
    <input type="text" name="search" placeholder="Search" required>
    <button class="btn" type="submit">Go</button>
</form>
{% if hits %}
    <p>Hits: {{ hits }} </p>
{% endif %}

{% if misses %}
    <p>Misses: {{ misses }} </p>
{% endif %}

{% if users %}
    <br>
    <ul>
    {% for user in users %}
    <li>{{ user['name'] }}
        <br>
        {{ user['email'] }}<br>
        {{ user['city'] }},
        {{ user['state'] }},
        {{ user['country'] }}
        </li>
    {% endfor %}
    </ul>
    {% endif %}
</div>
-->
'''

'''
@app.route('/look/')
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
'''


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

    return render_template('events.html', events=ee, hall_names=halls, hall_name=hall_name)