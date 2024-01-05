from django.core.management.base import BaseCommand

from sensor.tasks import import_to_db
from sensor.models import File


class Command(BaseCommand):
    help = "Import sensor files to the database"

    def handle(self, *args, **options):

        file_objs = File.objects.filter(parsed__isnull=True)
        for file_obj in file_objs:
            import_to_db(file_obj)
