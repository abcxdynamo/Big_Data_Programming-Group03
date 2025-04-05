from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps

from utils.time import utcnow

scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.start()

def interval_task(seconds):
    """
    Decorator: used to task tasks
    """
    def decorator(func):
        job_id = func.__name__
        @wraps(func)
        def wrapped(*args, **kwargs):
            print(f"-----job_id: {job_id} started. now: {utcnow()}")
            func(*args, **kwargs)
            print(f"-----job_id: {job_id} ended. now: {utcnow()}")
        # Add a task to the scheduler
        if not scheduler.get_job(job_id):
            scheduler.add_job(wrapped, 'interval', seconds=seconds, id=job_id, replace_existing=True)
            print(f"----add_job: {job_id}")

        return wrapped
    return decorator
