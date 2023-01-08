import json

users_path = r"data\users.json"


def open_file(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            return []


def write_file(file_path, changes):
    data = open_file(file_path)
    with open(file_path, 'w') as file:
        data.append(changes)
        json.dump(data, file, indent=4)


def check_user(student_number):
    """
    Checks whether a student number is already in the database
    :param student_number: str
    :return: bool
    """
    users_data = open_file(users_path)
    for user in users_data:
        if user['student_number'] == student_number:
            return True
    return False


def add_user(new_user_info):
    if not check_user(new_user_info['student_number']):
        print("Creating new user.")
        write_file(users_path, new_user_info)
        return True
    else:
        return False


def lookup_user(student_number):
    users_data = open_file(users_path)
    for user in users_data:
        if user['student_number'] == student_number:
            return user
