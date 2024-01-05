from celery import shared_task


@shared_task
def import_to_db(file_obj):
    file_obj.import_to_db()
