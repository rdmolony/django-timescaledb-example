from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Reading


class ReadingResource(resources.ModelResource):

    class Meta:
        model = Reading

class ReadingAdmin(ImportExportModelAdmin):
    resource_classes = [ReadingResource]

admin.site.register(Reading, ReadingAdmin)
