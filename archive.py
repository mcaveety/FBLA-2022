import json

import users
from users import open_file

users_path = r"data\users.json"
archive_toc_path = r"data\archive_toc.json"


def archive_file(session, file_path=users_path):
	"""
	Archives current leaderboard data
	:return: None
	"""
	archive_path = update_toc()
	data = users.assign_winners()
	with open(archive_path, 'x') as file:
		json.dump(data, file, indent=4)

	for user in data:
		if user.get('winner', None):
			user.pop('winner')
			user['credits'] = user['points']
		else:
			user['credits'] = 0
		user.update({
			'points': 0,
			'num_attended': 0,
			'events_attended': []
		})

	with open(file_path, 'w') as file:
		json.dump(data, file, indent=4)

	for user in data:
		if user['student_number'] == session['student_number']:
			return user


def initialize_toc(file_path=archive_toc_path):
	toc = open_file(file_path)
	try:
		toc = toc[0]
	except IndexError:
		toc = {}
	current_q = toc.get('current_q', 1)
	current_year = toc.get('current_year', 2020)
	current_qy = f"Q{current_q}{current_year}"
	toc.update({
		'current_q': current_q,
		'current_year': current_year,
		'current_qy': current_qy
	})
	toc = [toc]
	with open(file_path, 'w') as file:
		json.dump(toc, file, indent=4)


def update_toc(file_path=archive_toc_path):
	"""
	Updates current quarter and year
	Adds old data file path to a new key
	:param file_path: rstr
	:return: rstr
	"""
	toc = open_file(file_path)[0]
	current_q = toc.get('current_q', 1)
	current_year = toc.get('current_year', 2020)
	archive_qy = f"Q{current_q}{current_year}"
	archive_new_path = rf"data\users_{archive_qy}.json"

	if current_q == 2:
		current_q += 1
		current_year += 1
	elif current_q == 4:
		current_q = 1
	else:
		current_q += 1

	current_qy = f"Q{current_q}{current_year}"
	toc.update({
		'current_q': current_q,
		'current_year': current_year,
		'current_qy': current_qy,
		f'{archive_qy}': archive_new_path
	})
	toc = [toc]
	with open(file_path, 'w') as file:
		json.dump(toc, file, indent=4)

	return archive_new_path


def collect_paths(file_path=archive_toc_path):
	initialize_toc()
	toc = open_file(file_path)[0]
	for key in toc:
		if key == 'current_q' or key == 'current_year':
			continue
		elif key == 'current_qy':
			yield toc[key], users_path
		else:
			yield key, toc[key]
