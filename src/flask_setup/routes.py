
from src.flask_setup import app
from src.scheduler.scheduler import Scheduler
from src.scheduler.scheduler import AppReviewScheduler

from apscheduler.schedulers.background import BackgroundScheduler
import requests

def do():
    # Reddit Crawler Scheduler 
    scheduler = Scheduler(app.logger, requests)
    scheduler.get_datasets()
    scheduler.update_request_bodies()
    scheduler.make_crawler_requests()
    
    # App Review Crawler Scheduler
    app_scheduler = AppReviewScheduler(app.logger, requests)
    app_scheduler.get_datasets()
    app_scheduler.update_request_bodies()
    app_scheduler.make_crawler_requests()

sched = BackgroundScheduler(daemon=True)
sched.add_job(do,'interval',hours=24)
#sched.add_job(do,'interval',minutes=1)
sched.start()


if __name__ == "__main__":
    app.run()