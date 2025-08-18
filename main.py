from monitoring.watcher import FileWatcher
from monitoring.queue_manager import QueueManager
from parsing.parser import Parser


data_queue = QueueManager(name="FileDataQueue")
file_check = FileWatcher("loggings.txt", data_queue)

file_check.start()

while True:
    raw_data = data_queue.get(timeout=10)
    if raw_data:
        parsed = Parser()
        parsed.parse(raw_data)
        print(parsed.parsed_data)