import re


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




