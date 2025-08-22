import pymysql


class Db:
    def __init__(self):
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="dm3004^mk2606",
            database="shift_logger",
            cursorclass=pymysql.cursors.DictCursor
        )


    def get_connection(self):
        return self.connection