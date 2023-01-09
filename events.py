import json
from users import open_file, write_file

events_path = r"data\events.json"


def add_event_nums(file_path):
	data = open_file(file_path)
	for i, event in enumerate(data):
		event['event_num'] = i
	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)


def add_event_points(file_path):
	data = open_file(file_path)
	for event in data:
		if event['event_type'] == "Fun":
			event['event_points'] = 25
		elif event['event_type'] == "Sporting":
			event['event_points'] = 50
		elif event['event_type'] == "Art":
			event['event_points'] = 75
		elif event['event_type'] == "Academic":
			event['event_points'] = 100
	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)


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


add_event_points(events_path)