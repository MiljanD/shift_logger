

class Parser:
    def __init__(self):
        self.parsed_data = []


    def parse(self, log_data):
        for record in log_data:
            parsed_record = {}
            for rec in record.split(";"):
                parsed_rec = rec.split("=")
                parsed_record[parsed_rec[0].lower()] = parsed_rec[1]

            self.parsed_data.append(parsed_record)

