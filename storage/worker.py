from storage.database import Db
from utils.time_utils import convert_str_to_date, convert_datetime_to_date


class Worker(Db):
    def __init__(self):
        super().__init__()
        self.con = self.get_connection()
        self.idcard = None
        self.name = None


    @property
    def id_card(self):
        return self.idcard


    @id_card.setter
    def id_card(self, worker_idcard):
        self.idcard = worker_idcard


    @property
    def worker_name(self):
        return self.name


    @worker_name.setter
    def worker_name(self, name):
        self.name = name


    def generate_worker(self):
        if self.id_card is None or self.name is None:
            raise ValueError("ID card or name are not set.")

        with self.con.cursor() as cursor:
            query = "INSERT INTO workers (card_id, name) VALUES (%s, %s)"
            cursor.execute(query, (self.id_card, self.name))
            self.con.commit()



    def is_registered(self, idcard):
        with self.con.cursor() as cursor:
            query = "SELECT * FROM workers WHERE card_id=%s"
            cursor.execute(query, (idcard,))
            self.con.commit()

            result = cursor.fetchone()

        return result


    def is_checked_in(self, worker_id, time_stamp):
        current_date = convert_str_to_date(time_stamp)
        with self.con.cursor() as cursor:
            query = "SELECT id FROM logs WHERE worker_id=%s AND check_in=%s"
            cursor.execute(query, (worker_id, current_date))
            self.con.commit()

            result = cursor.fetchall()

        return result


    def check_in(self, worker_id, time_stamp):
            with self.con.cursor() as cursor:
                query = "INSERT INTO logs (worker_id, check_in) VALUES (%s, %s)"
                cursor.execute(query, (worker_id, time_stamp))
                self.con.commit()


    def check_out(self, worker_id, check_out_time):
        time_converted = convert_str_to_date(check_out_time)
        current_date = convert_datetime_to_date(time_converted)
        with self.con.cursor() as cursor:
            query = "UPDATE logs SET check_out = %s  WHERE worker_id = %s AND DATE(check_in) =%s"
            cursor.execute(query, (check_out_time, worker_id, current_date))
            self.con.commit()
