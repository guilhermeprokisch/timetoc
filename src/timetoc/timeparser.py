import datetime

import holidays
from dateutil.relativedelta import relativedelta


def parse_date_range(phrase, exclude_holidays=True, exclude_weekends=True):
    """
    Returns a list of datetime objects representing a date range based on a phrase describing the range.

    Parameters:
        phrase (str): A string describing the date range.
        exclude_holidays (bool): Whether to exclude Austrian public holidays from the resulting list of dates. Default is False.
        exclude_weekends (bool): Whether to exclude weekends (Saturdays and Sundays) from the resulting list of dates. Default is False.

    Returns:
        list: A list of datetime objects representing the dates in the range.
    """
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if phrase == "today":
        start_date = now
        end_date = now + datetime.timedelta(days=1)
    elif phrase == "yesterday":
        start_date = now - datetime.timedelta(days=1)
        end_date = now
    elif phrase == "tomorrow":
        start_date = now + datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=1)
    elif phrase == "this week":
        start_date = now - datetime.timedelta(days=now.weekday())
        end_date = start_date + datetime.timedelta(weeks=1)
    elif phrase == "last week":
        end_date = now - datetime.timedelta(days=now.weekday())
        start_date = end_date - datetime.timedelta(weeks=1)
    elif phrase == "next week":
        start_date = now + datetime.timedelta(days=(7 - now.weekday()))
        end_date = start_date + datetime.timedelta(weeks=1)
    elif phrase == "this month":
        start_date = now.replace(day=1)
        end_date = (start_date + relativedelta(months=1)).replace(day=1)
    elif phrase == "last month":
        end_date = now.replace(day=1)
        start_date = (end_date - relativedelta(months=1)).replace(day=1)

    date_range = []
    delta = datetime.timedelta(days=1)
    while start_date < end_date:
        if not exclude_weekends or start_date.weekday() not in [5, 6]:
            date_range.append(start_date)
        start_date += delta

    if exclude_holidays:
        at_holidays = holidays.AT(years=start_date.year)
        date_range = [
            d.strftime("%Y-%m-%d") for d in date_range if d not in at_holidays
        ]

    return date_range
