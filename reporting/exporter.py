from storage.database import Db
from utils.time_utils import convert_str_to_date, convert_datetime_to_date, get_week_range
from datetime import datetime


class Exporter(Db):
    def __init__(self):
        super().__init__()
        self.con = self.get_connection()


    def _execute_query(self, query, params=None):
        with self.con.cursor() as cursor:
            cursor.execute(query, params or ())
            self.con.commit()
            return cursor.fetchall()


    def export_all_logs(self):
        query = "SELECT * FROM logs"

        return self._execute_query(query)


    def export_all_workers(self):
        query = "SELECT * FROM workers"

        return self._execute_query(query)


    def export_logs_by_day(self, date=None):
        if date is None:
            current_date = datetime.now()
        else:
            current_date = convert_str_to_date(date)

        current_date = convert_datetime_to_date(current_date)

        query = "SELECT * FROM logs WHERE DATE(check_in) = %s"

        return self._execute_query(query, (current_date,))


    def export_weekly_logs(self, year=None, week=None):
        if year is None and week is None:
            current_year = datetime.now().year
            current_week = datetime.now().isocalendar().week
        else:
            current_year = year
            current_week = week


        start_of_week, end_of_week = get_week_range(current_year, current_week)
        start = datetime.combine(start_of_week, datetime.min.time())
        end = datetime.combine(end_of_week, datetime.max.time())

        query = "SELECT * FROM logs WHERE check_in BETWEEN %s AND %s"

        return self._execute_query(query, (start, end))


    def export_monthly_logs(self, year=None, month=None):
        if year is None and month is None:
            current_year = datetime.now().year
            current_month = datetime.now().month
        else:
            current_year = year
            current_month = month

        query = "SELECT * FROM logs WHERE MONTH(check_in) = %s AND YEAR(check_in) = %s"

        return self._execute_query(query, (current_month, current_year))

