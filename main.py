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

        validation = Validator()

        for record in parsed_raw_data:
            if validation.is_valid(record):
                pass
                # Pseudocode for rest of main loop
                # worker = Worker()
                # if worker.is_registered(record["card_id"]):
                #     worker.log_action(record)
                # else:
                #     worker.register(record)
                #     worker.log_action()


