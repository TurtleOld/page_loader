import tempfile

import requests
from requests_mock.mocker import Mocker

from page_loader import download
from page_loader.engine.download_content import download_images

link = 'https://python.org'
temp_dir = tempfile.TemporaryDirectory()
file_name = download(link, temp_dir.name)
file_name_tests = download(link, 'tests/fixtures')
links = download_images(link, 'tests/fixtures')


def test_download(requests_mock: Mocker):
    with open(file_name, 'r', encoding='utf-8') as file2:
        data = file2.read()
        requests_mock.get(link, text=data)

        assert data == requests.get(link).text


def test_download_images():
    path = 'python-org_files/-static-img-python-logo.png'
    assert path == links


# def test_change_links():
#     with open('tests/fixtures/python-org.html') as file_:
#         assert change_links(file_, links)

