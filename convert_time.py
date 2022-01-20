from dateutil.tz import gettz
from datetime import datetime

def convert_to_datetime(date_str):
    return datetime.strptime(date_str+"-0000", '%d/%m/%Y %H:%M:%S%z')


def convert_to_string(date):
    return date.strftime("%d/%m/%Y %H:%M:%S")


def convert_datetime_timezone_from_utc(date):
    return date.astimezone(gettz('America/Sao_Paulo'))


def convert_timestamp(date):
    return convert_to_string(convert_datetime_timezone_from_utc(convert_to_datetime(date)))


def sort_function(e):
  return e['timestamp']