from celery import shared_task


@shared_task
def echo():
    with open("echo.txt", "w") as f:
        f.write("Echo!")
