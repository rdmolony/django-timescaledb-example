import pytest
from django.conf import settings


@pytest.fixture(scope='function', autouse=True)
def media_root(tmp_path):
    original_media_root = settings.MEDIA_ROOT
    settings.MEDIA_ROOT = tmp_path / 'media'
    yield settings.MEDIA_ROOT
    settings.MEDIA_ROOT = original_media_root
