import json

users_path = r"data\users.json"


def open_file(file_path):
    """
    Opens a file and returns the data
    :param file_path: rstr
    :return: list
    """
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            return []


def write_file(file_path, changes):
    """
    Adds a dict to a JSON file
    :param file_path: rstr
    :param changes: dict
    :return: None
    """
    data = open_file(file_path)
    with open(file_path, 'w') as file:
        data.append(changes)
        json.dump(data, file, indent=4)


def update_user(file_path, student_num, changes):
    """
    Updates a user's attended events & point total
    :param file_path: rstr
    :param student_num: str
    :param changes: dict
    :return: None
    """
    data = open_file(file_path)
    with open(file_path, 'w') as file:
        for i, student in enumerate(data):
            if student_num == student['student_number']:
                data.pop(i)
                data.append(changes)

        json.dump(data, file, indent=4)


def add_attended(student_num, event_num, file_path=users_path):
    """
    Adds event to student's attended events
    :param student_num: str
    :param event_num: int
    :param file_path: rstr
    :return: None
    """
    data = open_file(file_path)
    for student in data:
        if student_num == student['student_number']:
            events_attended = student.get('events_attended', [])
            if event_num not in events_attended:
                events_attended.append(event_num)
            student['events_attended'] = events_attended
            update_user(file_path, student_num, student)


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
    """
    If a student number is not in use, creates a new account
    :param new_user_info:
    :return: Bool
    """
    if not check_user(new_user_info['student_number']):
        print("Creating new user.")
        write_file(users_path, new_user_info)
        return True
    else:
        return False


def lookup_user(student_number):
    """
    Looks up a user's data
    :param student_number: str
    :return: dict
    """
    users_data = open_file(users_path)
    for user in users_data:
        if user['student_number'] == student_number:
            return user
