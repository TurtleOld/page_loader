import os
import tempfile

import pytest
import requests_mock

from page_loader import download
from page_loader.engine.download_content import create_folder

URL = 'https://page-loader.hexlet.repl.co'

url_image = os.path.join(URL, 'assets/professions/nodejs.png')

downloads_dir = os.path.join('tests', 'fixtures', 'downloads')

html_file_name = 'page-loader-hexlet-repl-co.html'
created_dir_name = 'page-loader-hexlet-repl-co_files'
image_name = 'page-loader.hexlet-repl-co--assets-professions-nodejs.png'

created_html_file = os.path.join(downloads_dir,
                                 html_file_name)
created_image = os.path.join(created_dir_name, image_name)

expected_image = os.path.join(downloads_dir, created_image)


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


def test_folder_creation():
    folder = create_folder(URL, downloads_dir)
    assert os.path.join(downloads_dir, folder) == os.path.join(downloads_dir,
                                                               created_dir_name)


parametrize_exist = [
    html_file_name,
    created_image
]


@pytest.mark.parametrize('expected', parametrize_exist)
def test_download_content(expected):
    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(URL, content=read_file(created_html_file))
        mock.get(url_image, content=read_file(expected_image))
        with tempfile.TemporaryDirectory() as directory:
            download(URL, directory)
            expected_path = os.path.join(directory, expected)
            assert os.path.exists(expected_path)
