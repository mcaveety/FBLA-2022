import json
from users import open_file, write_file

prizes_path = r"data\prizes.json"


def add_prize(file_path=prizes_path):
	new_prize = {
		'name': input("name:"),
		'desc': input("desc:"),
		'type': input("type:"),
		'img_url': rf"static\{input('url:')}",
		'credits': int(input("credits:"))
	}
	write_file(file_path, new_prize)


def get_prizes(file_path=prizes_path):
	return open_file(file_path)

