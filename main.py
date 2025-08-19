from monitoring.watcher import FileWatcher
from monitoring.queue_manager import QueueManager
from parsing.parser import Parser
from parsing.validator import Validator


data_queue = QueueManager(name="FileDataQueue")
file_check = FileWatcher("loggings.txt", data_queue)

file_check.start()

while True:
    raw_data = data_queue.get(timeout=10)
    if raw_data:
        parsed = Parser()
        parsed.parse(raw_data)
        parsed_raw_data = parsed.parsed_data
        print(parsed_raw_data)
        is_valid = Validator()
        keys_value = []
        for record in parsed_raw_data:
            keys_value.append(is_valid.check_keys(record))
        print(keys_value)
