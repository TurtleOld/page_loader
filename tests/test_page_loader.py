import tempfile

from requests_mock.mocker import Mocker

from page_loader import download

link = 'https://python.org'
temp_dir = tempfile.TemporaryDirectory()
file_name = download(link, temp_dir.name)
file_name_tests = download(link, 'tests/fixtures')
# links = download_images(link, 'tests/fixtures')


def test_download(requests_mock: Mocker):
    pass
