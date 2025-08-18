import threading
import time


class FileWatcher(threading.Thread):
    def __init__(self, path, queue):
        super().__init__(daemon=True)
        self.path = path
        self.queue = queue
        self.file_len = 0



    def run(self):
        while True:
            log_data = self.check_file()
            if log_data:
                self.queue.put(log_data)
            time.sleep(5)


    def check_file(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                lines = [line.strip() for line in lines]

            if len(lines) > self.file_len:
                new_data = lines[self.file_len:]
                self.file_len = len(lines)
                return new_data
            return None

        except FileNotFoundError:
            print(f"File not found: {self.path}")
            return None

