from celery import shared_task

from . import io


@shared_task
def import_to_db(file_obj):
    io.import_to_db(file_obj)
