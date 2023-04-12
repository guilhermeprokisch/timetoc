import os
from datetime import datetime

import requests

TIME_TRACK_BASE_URL = os.environ["TIME_TRACK_BASE_URL"]


def make_headers(token=None):
    return {
        "Authorization": f"Bearer {token}",
    }


def add_time_entry(
    day="2023-03-14",
    start_time="09:10",
    end_time="12:00",
    break_time=False,
    token=None,
):
    headers = make_headers(token)

    task_id = 4
    if break_time:
        task_id = 9

    data = {
        "0": {
            "user_id": 556,
            "task_id": task_id,
            "start_time_timezone": "Europe/Vienna",
            "end_time_timezone": "Europe/Vienna",
            "start_time": f"{day} {start_time}:00",
            "end_time": f"{day} {end_time}:00",
            "notes": "",
            "start_type_id": "0",
            "end_type_id": "0",
        },
    }

    response = requests.post(
        f"{TIME_TRACK_BASE_URL}/userapi/v3/timeTrackings/create/",
        headers=headers,
        json=data,
    )

    response.raise_for_status()

    if response.status_code == 200:
        if break_time:
            print(
                f"✅ Break time entry starting at {start_time} ending at {end_time}  add successfully ☕ "
            )
            return

        print(
            f"✅ Time entry starting at {start_time} ending at {end_time}  add successfully 🕒"
        )


def add_home_office(day, token):
    headers = make_headers(token)
    data = {
        "user_id": "556",
        "subtype_id": "12",
        "type_id": "3",
        "from_date": f"{day}",
        "to_date": f"{day}",
        "request_duration_entity": "d",
        "duration": "1",
        "request_comment": "",
    }

    response_home_office = requests.post(
        f"{TIME_TRACK_BASE_URL}/userapi/v3/absences/create/",
        headers=headers,
        data=data,
    )
    if response_home_office.status_code == 200:
        print("✅ Home office entry add successfully 🏠")


def add_work_day(day, start, finish, break_start, break_finish, is_home_office, token):
    add_time_entry(day, start_time=start, end_time=break_start, token=token)
    add_time_entry(
        day, start_time=break_start, end_time=break_finish, break_time=True, token=token
    )
    add_time_entry(day, start_time=break_finish, end_time=finish, token=token)
    if is_home_office:
        add_home_office(day, token)

    work_time = total_work_time(start, finish, break_start, break_finish)
    print(f"Total work time on {day} -> {work_time} hours ")


def hours_difference(start, end):
    t1 = datetime.strptime(start, "%H:%M")
    t2 = datetime.strptime(end, "%H:%M")
    return t2 - t1


def total_work_time(start, finish, break_start, break_finish):
    working_time_1 = hours_difference(start, break_start)
    working_time_2 = hours_difference(break_finish, finish)
    total_work_time = working_time_1 + working_time_2
    hours_diff = "{:0>8}".format(str(total_work_time))
    return hours_diff
