import os
import tempfile

import pytest
import requests_mock

from page_loader import download
from page_loader.engine.download_content import create_folder, get_content

URL = 'https://page-loader.hexlet.repl.co'
internet_path_image = 'assets/professions/nodejs.png'
internet_path_css = 'assets/application.css'
internet_path_js = 'script.js'
url_image = os.path.join(URL, internet_path_image)
url_css = os.path.join(URL, internet_path_css)
url_js = os.path.join(URL, internet_path_js)

path_original = os.path.join('tests', 'fixtures', 'downloads')
downloads_dir = os.path.join('tests', 'fixtures', 'downloads', 'changed')

html_file_name = os.path.join(path_original, 'page-loader-hexlet-repl-co.html')
changed_html_file_name = 'page-loader-hexlet-repl-co.html'
created_dir_name = 'page-loader-hexlet-repl-co_files'
image_name = 'page-loader-hexlet-repl-co--assets-professions-nodejs.png'
css_name = 'page-loader-hexlet-repl-co--assets-application.css'
js_name = 'page-loader-hexlet-repl-co--script.js'


created_html_file = os.path.join(downloads_dir, changed_html_file_name)
created_image = os.path.join(created_dir_name, image_name)
created_css = os.path.join(created_dir_name, css_name)
created_js = os.path.join(created_dir_name, js_name)

expected_image = os.path.join(downloads_dir, created_image)
expected_css = os.path.join(downloads_dir, created_css)
expected_js = os.path.join(downloads_dir, created_js)


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


def test_folder_creation():
    folder = create_folder(URL, downloads_dir)
    assert os.path.join(downloads_dir, folder) == os.path.join(downloads_dir,
                                                               created_dir_name)


@pytest.mark.parametrize('expected', [
    changed_html_file_name,
    created_image,
    created_css,
    created_js
])
def test_download_content(expected):
    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(URL, content=read_file(created_html_file))
        mock.get(url_image, content=read_file(expected_image))
        mock.get(url_css, content=read_file(expected_css))
        mock.get(url_js, content=read_file(expected_js))
        with tempfile.TemporaryDirectory() as directory:
            download(URL, directory)
            expected_path = os.path.join(directory, expected)
            assert os.path.exists(expected_path)


@pytest.mark.parametrize('new_file, old_file', [
    (changed_html_file_name, html_file_name),
])
def test_change_html_file(new_file, old_file):
    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(URL, content=read_file(created_html_file))
        with tempfile.TemporaryDirectory() as directory:
            download(URL, directory)
            file = os.path.join(directory, new_file)
            assert read_file(file) != read_file(old_file)


def test_get_content():
    result = get_content(URL, path_original)
    assert result == html_file_name
