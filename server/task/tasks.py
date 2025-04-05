import time
from task import interval_task
from task.grade_prediction import predict_and_update_gpa
from utils.time import utcnow


# @interval_task(3)  # Execute a task every 3 seconds
def scheduled_test():
    print(f"Task execution time: {utcnow()}")


@interval_task(60)  # Execute a task every 60 seconds
def scheduled_predict_and_update_gpa():
    predict_and_update_gpa()
