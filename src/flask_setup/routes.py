
from src.flask_setup import app
from src.scheduler.scheduler import Scheduler

from apscheduler.schedulers.background import BackgroundScheduler
import requests

def do():
    scheduler = Scheduler(app.logger, requests)
    scheduler.get_datasets()
    scheduler.update_request_bodies()
    scheduler.make_crawler_requests()

sched = BackgroundScheduler(daemon=True)
sched.add_job(do,'interval',hours=24)
sched.start()


if __name__ == "__main__":
    app.run()