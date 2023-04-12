"""A command-line tool for tracking work time in timetoc.

This module provides functions to add work days and get the corresponding time tracking 
information using the timetoc API. It uses the typer module for the command-line interface, 
keyring for storing login information securely, and rich for pretty-printing information.

Functions:
    access_token_by_login: Retrieves access token from timetoc by logging in and 
        authenticating the user.
    get_day_info: Retrieves user input for work day information such as start and finish time,
        break start and finish time, whether the day is a home office day, and the day's date.
    add_work_day_with_retry: Adds a work day to the timetoc server with a retry mechanism in 
        case the authentication token has expired.
    main: The main function that runs the command-line interface.
"""

from datetime import datetime

import keyring
import typer
from rich.console import Console
from rich.prompt import Prompt

from timetoc.login import get_access_token
from timetoc.timeparser import parse_date_range
from timetoc.timetracking import add_work_day

app = typer.Typer()
console = Console()

# Constants
HEADLESS_LOGIN_DEFAULT = False
START_TIME_DEFAULT = "09:00"
FINISH_TIME_DEFAULT = "17:30"
BREAK_START_DEFAULT = "12:30"
BREAK_FINISH_DEFAULT = "13:00"
HOMEOFFICE_DAYS_DEFAULT = ["Tuesday", "Thursday"]


def access_token_by_login():
    """Retrieve access token from timetoc by logging in and authenticating the user.

    The function first prompts the user to select whether to use a headless login or not. If
    headless login is selected, the function retrieves the user's email and password from the
    system's keyring. If the email and password are not stored, the function prompts the user to
    enter them and saves them to the keyring if the user chooses to do so. The function then calls
    the get_access_token function to retrieve the access token using the provided email, password,
    and headless parameters.

    Returns:
        str: The retrieved access token.
    """

    headless_login = typer.confirm("Headless login?", default=HEADLESS_LOGIN_DEFAULT)

    if headless_login:
        email = keyring.get_password("system", "timetoc_email")
        password = keyring.get_password("system", "timetoc_password")

        if not email or not password:
            email = Prompt.ask("Email")
            password = Prompt.ask("Password", password=True)
            save_pass = typer.confirm("Save Login and Password?", default=True)

            if save_pass:
                keyring.set_password("system", "timetoc_email", email)
                keyring.set_password("system", "timetoc_password", password)

        access_token = get_access_token(email=email, password=password, headless=True)
    else:
        access_token = get_access_token(headless=False)

    return access_token


def get_additional_info(
    day,
    start,
    finish,
    break_start,
    break_finish,
    is_home_office,
):
    """Retrieve user input for work day information.

    The function prompts the user to enter the start and finish time, break start and finish time,
    and whether the day is a home office day. The function then returns a tuple containing the
    start and finish time, break start and finish time, the week day name of the day (e.g.,
    Monday, Tuesday, etc.), and whether the day is a home office day.

    Args:
        day (str): The date of the work day in the format yyyy-mm-dd.

    Returns:
        Tuple[str, str, str, str, str, bool]: A tuple containing the start and finish time, break
        start and finish time, the week day name of the day, and whether the day is a home office
        day.
    """

    day_datetime = datetime.strptime(day, "%Y-%m-%d")
    week_day_name = day_datetime.strftime("%A")
    if not start:
        start = Prompt.ask("Start Time", default=START_TIME_DEFAULT)
    if not finish:
        finish = Prompt.ask("Finish Time", default=FINISH_TIME_DEFAULT)
    if not break_start:
        break_start = Prompt.ask("Break Start", default=BREAK_START_DEFAULT)
    if not break_finish:
        break_finish = Prompt.ask("Break Finish", default=BREAK_FINISH_DEFAULT)
    if not is_home_office:
        is_home_office = False if week_day_name in HOMEOFFICE_DAYS_DEFAULT else True
        is_home_office = typer.confirm("Is Home Office?", default=is_home_office)

    return start, finish, break_start, break_finish, week_day_name, is_home_office


def add_work_day_with_retry(
    day, start, finish, break_start, break_finish, is_home_office, access_token
):
    """Add a work day to the timetoc server with a retry mechanism in case the authentication
    token has expired.

    The function first calls the add_work_day function to add the work day with the provided
    parameters and access token. If an exception is raised due to an expired authentication token,
    the function retrieves a new access token by calling the access_token_by_login function and
    then calls add_work_day again with the new access token.

    Args:
        day (str): The date of the work day in the format yyyy-mm-dd.
        start (str): The start time of the work day in the format hh:mm.
        finish (str): The finish time of the work day in the format hh:mm.
        break_start (str): The start time of the break in the work day in the format hh:mm.
        break_finish (str): The finish time of the break in the work day in the format hh:mm.
        is_home_office (bool): Whether the day is a home office day or not.
        access_token (str): The authentication token to access the timetoc API.
    """

    try:
        add_work_day(
            day=day,
            start=start,
            finish=finish,
            break_start=break_start,
            break_finish=break_finish,
            is_home_office=is_home_office,
            token=access_token,
        )
    except:
        console.print("❌ Token expired please login again")
        access_token = access_token_by_login()
        add_work_day(
            day=day,
            start=start,
            finish=finish,
            break_start=break_start,
            break_finish=break_finish,
            is_home_office=is_home_office,
            token=access_token,
        )


@app.command()
def main(
    day: str = typer.Option(
        None, "--day", "-d", help="The date of the work day in the format yyyy-mm-dd."
    ),
    day_str: str = typer.Option(
        None,
        "--day-str",
        "-ds",
        help="The date of the work day in natural languge. E.g 'today, yesterday'",
    ),
    start: str = typer.Option(
        None,
        "--start",
        "-s",
        help="The start time of the work day in the format hh:mm.",
    ),
    finish: str = typer.Option(
        None,
        "--finish",
        "-f",
        help="The finish time of the work day in the format hh:mm.",
    ),
    break_start: str = typer.Option(
        None,
        "--break-start",
        "-bs",
        help="The start time of the break in the work day in the format hh:mm.",
    ),
    break_finish: str = typer.Option(
        None,
        "--break-finish",
        "-bf",
        help="The finish time of the break in the work day in the format hh:mm.",
    ),
    is_home_office: bool = typer.Option(
        None,
        "--home-office",
        "-h",
        help="Whether the day is a home office day.",
    ),
):
    access_token = keyring.get_password("system", "timetoc_access_token")

    if not access_token:
        console.print("Access token not found!", style="red")
        access_token = access_token_by_login()

    days = []

    if not day_str and not day:
        day_str = Prompt.ask("Day String", default="yesterday")

    if not day and day_str:
        days = parse_date_range(day_str)

    if day and not day_str:
        days = [day]

    for day in days:
        (
            start,
            finish,
            break_start,
            break_finish,
            week_day_name,
            is_home_office,
        ) = get_additional_info(
            day, start, finish, break_start, break_finish, is_home_office
        )

        console.print("Day: ", f"{day} {week_day_name}", style="bold red")

        add_work_day_with_retry(
            day=day,
            start=start,
            finish=finish,
            break_start=break_start,
            break_finish=break_finish,
            is_home_office=is_home_office,
            access_token=access_token,
        )


if __name__ == "__main__":
    app()
