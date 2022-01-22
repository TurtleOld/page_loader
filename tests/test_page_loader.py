import tempfile

import requests
from requests_mock.mocker import Mocker

from page_loader import download

link = 'https://ru.hexlet.io/courses'
temp_dir = tempfile.TemporaryDirectory()
file_name = download(link, temp_dir.name)


def test_download(requests_mock: Mocker):
    with open(file_name, 'r', encoding='utf-8') as file2:
        data = file2.read()
        requests_mock.get(link, text=data)

        assert data == requests.get(link).text
