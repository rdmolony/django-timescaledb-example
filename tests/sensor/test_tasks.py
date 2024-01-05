from unittest.mock import Mock

from sensor.models import File
from sensor.tasks import import_to_db


def test_import_to_db_is_called():

    file_obj = File()
    file_obj.import_to_db = Mock()
    import_to_db(file_obj)
    file_obj.import_to_db.assert_called()
