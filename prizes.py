import users
from users import write_file

prizes_path = users.resource_path(r"data\prizes.json")


def add_prize(file_path=prizes_path):
	"""
	Adds new prize to database
	:param file_path:
	:return: None
	"""
	new_prize = {
		'name': input("name:"),
		'desc': input("desc:"),
		'type': input("type:"),
		'img_url': rf"static\{input('url:')}",
		'credits': int(input("credits:"))
	}

	write_file(file_path, new_prize)
