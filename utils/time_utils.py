from datetime import datetime, timedelta, date

def convert_str_to_date(str_date):
    str_format = "%Y-%m-%dT%H:%M:%S"
    converted_date = datetime.strptime(str_date, str_format)

    return converted_date


def convert_datetime_to_date(datetime_obj):
    converted_date = datetime_obj.date()
    return converted_date


def check_date(first_datetime, second_datetime):
    first = first_datetime.date()
    second = second_datetime.date()

    if first == second:
        return True
    else:
        return False


def get_week_range(year, week):
    start_day = date.fromisocalendar(year, week, 1)
    end_day = start_day + timedelta(days=6)

    return start_day, end_day








