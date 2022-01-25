import tempfile

import requests
from requests_mock.mocker import Mocker

from page_loader import download
from page_loader.engine.download_content import download_images

link = 'https://python.org'
temp_dir = tempfile.TemporaryDirectory()
file_name = download(link, temp_dir.name)
links = download_images(link, 'fixtures')


def test_download(requests_mock: Mocker):
    with open(file_name, 'r', encoding='utf-8') as file2:
        data = file2.read()
        requests_mock.get(link, text=data)

        assert data == requests.get(link).text


def test_download_images():
    paths = 'tests/fixtures/python-org_files/-static-img-python-logo.png'
    assert paths == links
