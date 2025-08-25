
from monitoring.watcher import FileWatcher
from monitoring.queue_manager import QueueManager
from parsing.parser import Parser
from parsing.validator import Validator
from storage.worker import Worker


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
        worker = Worker()

        for record in parsed_raw_data:
            if validation.is_valid(record):

                current_worker = worker.is_registered(record["card_id"])
                if current_worker:
                    checked_in = worker.is_checked_in(current_worker["id"], record["time"])
                    if record["action"] == "IN":
                        if not checked_in:
                            worker.check_in(current_worker["id"], record["time"])
                    else:
                        worker.check_out(current_worker["id"], record["time"])
                else:
                    worker.worker_name = record["name"]
                    worker.id_card = record["card_id"]
                    worker.generate_worker()
