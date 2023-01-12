import json
import random

users_path = r"data\users.json"
events_path = r"data\events.json"


def open_file(file_path=users_path):
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
                break

        json.dump(data, file, indent=4)


def add_attended(student_num, event_num, users_fpath=users_path, events_fpath=events_path):
    """
    Adds event to student's attended events
    :param student_num: str
    :param event_num: int
    :param users_fpath: rstr
    :param events_fpath: rstr
    :return: None
    """
    user_data = open_file(users_fpath)
    event_data = open_file(events_fpath)

    # Find the student's data
    for student in user_data:
        if student_num == student['student_number']:

            # Add non-duplicate event to attended list
            events_attended = student.get('events_attended', [])
            if event_num not in events_attended:
                # Add event
                events_attended.append(event_num)

                # Add 1 to total attended
                student['num_attended'] += 1

                # Add points to user
                points = student.get('points', 0)
                points += get_points(event_data, event_num)
                student['points'] = points

            student['events_attended'] = events_attended

            update_user(users_fpath, student_num, student)
            break


def get_points(event_data, event_num):
    """
    Calculates how many points the user has
    :attended: list
    :file_path: rstr
    :return: None
    """
    # Load both files
    for event in event_data:
        if event_num == event['num']:
            return event['points']


def assign_winners(file_path=users_path):
    user_data = open_file(file_path)
    top_user = user_data[0]
    pos = 0
    for i in range(len(user_data)):
        if user_data[i]['points'] > top_user['points']:
            top_user = user_data[i]
            pos = i
    user_data[pos]['winner'] = True

    grade_levels = ["9", "10", "11", "12"]
    winners_index_list = []
    for i in range(len(grade_levels)):
        temp_list = []
        grade_level = grade_levels[i]
        for i, user in enumerate(user_data):
            if user.get('winner', None):
                continue
            elif grade_level == user['grade_level']:
                temp_list.append(i)
        if len(temp_list) > 0:
            print(temp_list)
            winners_index_list.append(temp_list[random.randrange(0, len(temp_list))])

    for i, user in enumerate(user_data):
        if i in winners_index_list:
            user['winner'] = True
    return user_data



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
        new_user_info.update({
            'points': 0,
            'credits': 0,
            'num_attended': 0,
            'events_attended': []
        })
        write_file(users_path, new_user_info)
        return True
    else:
        return False


def sort_leaderboard(file_path=users_path):
    user_data = open_file(file_path)
    sorted_data = []
    for i in range(len(user_data)):
        pos = 0
        top_user = user_data[0]
        for j in range(len(user_data)):
            if user_data[j]['points'] > top_user['points']:
                top_user = user_data[j]
                pos = j
        user_data.pop(pos)
        sorted_data.append(top_user)
    return sorted_data


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
