
from monitoring.watcher import FileWatcher
from monitoring.queue_manager import QueueManager
from parsing.parser import Parser
from parsing.validator import Validator
from storage.worker import Worker
from reporting.generator import ReportGenerator
from datetime import datetime, timedelta


data_queue = QueueManager(name="FileDataQueue")
file_check = FileWatcher("loggings.txt", data_queue)

file_check.start()

report = ReportGenerator()

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

    today = datetime.now()

    if today.hour == 0:
        report.generate_daily_pdf_report(current_date=datetime.now() - timedelta(days=1))

    if today.weekday() == 0 and today.hour == 0:
        last_week = today - timedelta(weeks=1)
        year, week = last_week.isocalendar()[:2]
        report.generate_weekly_report(year, week)

    if today.day == 1 and today.hour == 0:
        last_month = today.replace(day=1) - timedelta(days=1)
        report.generate_monthly_report(year=last_month.year, month=last_month.month)
