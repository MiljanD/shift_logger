import queue
from queue import Queue
import logging


class QueueManager:
    def __init__(self, maxsize=0, name="MainQueue"):
        self.queue = Queue(maxsize=maxsize)
        self.name = name
        self.processed_count = 0
        logging.basicConfig(level=logging.INFO)


    def put(self, item):
        try:
            self.queue.put(item, timeout=2)
            logging.info(f"Inserted into {self.name}: {item}")
        except queue.Full:
            logging.warning(f"{self.name} is full. Item is not inserted.")


    def get(self, timeout=5):
        try:
            item = self.queue.get(timeout=timeout)
            self.processed_count += 1
            logging.info(f"From {self.name}, item {item} is taken")
            return item
        except queue.Empty:
            logging.debug(f"{self.name} queue is empty.")
            return None

    def size(self):
        return self.queue.qsize()


    def stats(self):
        return {
            "name": self.name,
            "size": self.size(),
            "processed": self.processed_count
        }
