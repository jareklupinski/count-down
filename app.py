import os

from datetime import datetime
from dotenv import load_dotenv
from urllib import request

from flask import Flask
from icalendar import Calendar

app = Flask(__name__)
load_dotenv('.env')

@app.route("/")

def index():
    calendar_url = os.environ.get('CALENDAR_URL')
    if calendar_url is None:
        return "Invalid Calendar URL!"
    
    response = request.urlopen(calendar_url)
    if response.status != 200:
        return "Invalid Status from Calendar Server!"
    
    data = response.read()
    if len(data) < 5:
        return "No Data Received from Calendar Server!"
    
    try:
        cal = Calendar.from_ical(data)
    except Exception as e:
        return e
    
    timestamp_now = datetime.now().timestamp()
    timestamp_soonest = float('inf')
    
    for event in cal.walk('vevent'):
        try:
            timestamp_temp = event.get('dtstart').dt.timestamp()
        except:
            pass
        else:
            if timestamp_temp < timestamp_now:
                continue
            if timestamp_temp < timestamp_soonest:
                timestamp_soonest = timestamp_temp
    
    return str(timestamp_soonest)
    