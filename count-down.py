import icalendar
from datetime import datetime
with open('basic.ics', 'rb') as fp:
	data = fp.read()
cal = Calendar.from_ical(data)
timestamp_now = datetime.now()
timestamp_soonest = float('inf')
for event in cal.walk('vevent'):
	timestamp_temp = event.get('dtstart').dt.timestamp()
	if timestamp_temp < timestamp_now:
		# event already happened, skip
		continue
	if timestamp_temp < timestamp_soonest:
		# event is sooner than the soonest tracked event
		timestamp_soonest = timestamp_temp
print(timestamp_soonest)