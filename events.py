import json

from users import open_file, write_file

events_path = r"data\events.json"


# Used to initially format event data
def add_event_nums(file_path=events_path):
	"""
	Adds numbers to all events for identification
	:param file_path: rstr
	:return: None
	"""
	data = open_file(file_path)

	for i, event in enumerate(data):
		event['num'] = i

	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)


def add_event_points(file_path=events_path):
	"""
	Assigns points based off of event type
	:param file_path: rstr
	:return: None
	"""
	data = open_file(file_path)

	for event in data:
		if event['type'] == "Fun":
			event['points'] = 25
		elif event['type'] == "Sporting":
			event['points'] = 50
		elif event['type'] == "Art":
			event['points'] = 75
		elif event['type'] == "Academic":
			event['points'] = 100

	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)


def add_event(file_path=events_path):
	"""
	Adds new event to database
	:return: None
	"""
	event_info = {
		'name': input("Event name:"),
		'desc': input("Event desc:"),
		'type': input("Event type:"),
		'date': input("Event date:"),
		'time': input("Event time:")
	}

	write_file(file_path, event_info)


def load_events():
	return open_file(events_path)

