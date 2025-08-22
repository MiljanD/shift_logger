import re
import datetime
import logging
from utils.time_utils import convert_str_to_date

class Validator:
    def __init__(self):
        self.required_keys = ["card_id", "name", "time", "action"]


    def check_keys(self, record):
        are_keys = True
        for key, value in record.items():
            if key not in self.required_keys:
                are_keys = False

        return are_keys


    def check_idcard_type(self, record):
        is_card_type = True
        if not record['card_id'].isdigit():
            is_card_type = False

        return is_card_type


    def check_name_type(self, record):
        name_pattern = r"^[A-Z][a-z]+(([' -][A-Z][a-z]+)|([A-Z][a-z]*'[A-Z][a-z]+))*$"

        name_type = False

        if re.match(name_pattern, record["name"]):
            name_type = True

        return name_type


    def check_date_stamp(self, record):
        date_str = record["time"]

        try:
            converted_date = convert_str_to_date(date_str)
            return isinstance(converted_date, datetime.datetime)
        except (ValueError, TypeError):
            logging.warning("Wrong date format.")
            return False


    def check_action(self, record):
        actions = ["IN", "OUT"]
        is_valid_action = True
        if record["action"] not in actions:
            is_valid_action = False

        return is_valid_action


    def is_valid(self, record):
        return(
            self.check_keys(record) and
            self.check_idcard_type(record) and
            self.check_date_stamp(record) and
            self.check_name_type(record) and
            self.check_action(record)
        )



if __name__ == "__main__":
    validation = Validator()
    is_valid = validation.is_valid({'card_id': '1001', 'name': 'Petar Petrovic', 'time': '2025-08-18T07:55:00', 'action': 'IN'})
    print(is_valid)





