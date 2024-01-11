from celery import shared_task

from .models import File


@shared_task
def parse_and_import_to_db(file_id):
    file_obj = File.objects.get(id=file_id)
    file_obj.parse_and_import_to_db()
