import json
from users import open_file, write_file

events_path = r"data\events.json"


def add_event():
	event_info = {
		'event_name': input("Event name:"),
		'event_desc': input("Event desc:"),
		'event_type': input("Event type:"),
		'event_date': input("Event date:"),
		'event_time': input("Event time:")
	}
	write_file(events_path, event_info)


def load_events():
	return open_file(events_path)
