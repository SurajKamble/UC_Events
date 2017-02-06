import connections
import re

from flask import Flask
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(80)
from google.appengine.ext import vendor
# Add any libraries installed in the "lib" folder.
vendor.add('lib')
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import lxml
import lxml.etree
app = Flask(__name__)
c, conn = connections.connection()

a = "Suraj Kamble"
a = a.split()
print(a[0])


class events:

    def __init__(self, event_name, location, description, time):
        self.event_name = event_name
        self.location = location
        self.description = description
        self.time = time

    def get_all(self):

        print("Event_name: " + self.event_name)
        print("Location: " + self.location)
        print("Description: " + self.description)
        print("Time: " + self.time)
        print("\n--------------------------------\n")

    def get(self):
        aaa = "\n Event_name: " + self.event_name + "Location: " + self.location +  "Description: " + self.description + "Time: " + self.time + "\n--------------------------------\n"

        return aaa

page = urlfetch.fetch('http://calendar.uc.edu/wv3/wv3_servlet/urd/run/wv_event.WeekList?evdt=20160318,evfilter=6854,ebdviewmode=grid')

# page = requests.get('http://calendar.uc.edu/wv3/wv3_servlet/urd/run/wv_event.WeekList?evfilter=6854,evdt=20160209')

soup = BeautifulSoup(page.content, "lxml")
count = 0
all_events = []
for one in soup.find_all('a'):
    x = one.get('href')
    '''
    if count >= 15:
        break
    '''
    if x.startswith('javascript:rsrvInfo'):
        y = re.findall("\d+", x)
        a = ''.join(y)
        count += 1
        '''
        print("Event ID: " + a)
        print(" count: " + str(count))
        '''
        event_page = urlfetch.fetch('http://calendar.uc.edu/wv3/wv3_servlet/urd/run/wv_event.Detail?id='+a)
        event_soup = BeautifulSoup(event_page.content, "lxml")
        n = event_soup.find("div", "DetailName")
        l = event_soup.find("a", "RolloverLink")
        d = "Description"
        t = event_soup.find("td", "DetailBody")
        name = n.text.strip()
        loc = l.text.strip()
        desc = d
        t = t.text.strip()
        a = events(name, loc, desc, t)
        a.get_all()
        all_events.append(a)
hall_names = []
for a in all_events:
    l = a.location
    if l != "":
        l = l.split()
        hall_names.append(l[0])
        print(l[0])
hall_names = list(set(hall_names))
print("hall name : ")
print(hall_names)


b = []

for a in all_events:
    loc = a.location
    if loc.startswith('OLDCHEM'):
        print("Events in Old Chem: ")
        a.get_all()
        b.append(a)


def load_halls(hall_names):

    conn.commit()
    for hall in hall_names:
        c.execute("INSERT INTO hall (hall_name, hall_title) VALUES (%s, %s)", (hall, hall))
    conn.commit()


def load_events(all_events):

    description = "Des"
    for event in all_events:
        hall_name = event.location
        if hall_name != "":
            hall_name = hall_name.split()
            hall_name = hall_name[0]
            event_name = event.event_name
            location = event.location
            event_time = event.time
            print("Hall_name: ")
            print(hall_name)

            c.execute("INSERT INTO events (event_name, location, event_time, description, hall_name) "
                      "VALUES (%s, %s, %s, %s, %s)", (event_name, location, event_time, description, hall_name))
            conn.commit()

c.execute("DELETE FROM events")
c.execute("DELETE FROM hall")
load_halls(hall_names)
load_events(all_events)