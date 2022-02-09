import os
import tempfile

import pytest
import requests_mock

from page_loader import download
from page_loader.engine.download_content import create_folder, get_html_file, \
    get_content

URL = 'https://page-loader.hexlet.repl.co'
INVALID_URL = 'https://badsite.com'
INTERNET_PATH_IMAGE = 'assets/professions/nodejs.png'
INTERNET_PATH_CSS = 'assets/application.css'
INTERNET_PATH_JS = 'script.js'
URL_IMAGE = os.path.join(URL, INTERNET_PATH_IMAGE)
URL_CSS = os.path.join(URL, INTERNET_PATH_CSS)
URL_JS = os.path.join(URL, INTERNET_PATH_JS)

PATH_ORIGINAL = os.path.join('tests', 'fixtures', 'downloads')
DOWNLOADS_DIR = os.path.join('tests', 'fixtures', 'downloads', 'changed')

HTML_FILE_NAME = os.path.join(PATH_ORIGINAL, 'page-loader-hexlet-repl-co.html')
CHANGED_HTML_FILE_NAME = 'page-loader-hexlet-repl-co.html'
CREATED_DIR_NAME = 'page-loader-hexlet-repl-co_files'
IMAGE_NAME = 'page-loader-hexlet-repl-co--assets-professions-nodejs.png'
CSS_NAME = 'page-loader-hexlet-repl-co--assets-application.css'
JS_NAME = 'page-loader-hexlet-repl-co---script.js'

CREATED_HTML_FILE = os.path.join(DOWNLOADS_DIR, CHANGED_HTML_FILE_NAME)
CREATED_IMAGE = os.path.join(CREATED_DIR_NAME, IMAGE_NAME)
CREATED_CSS = os.path.join(CREATED_DIR_NAME, CSS_NAME)
CREATED_JS = os.path.join(CREATED_DIR_NAME, JS_NAME)

EXPECTED_IMAGE = os.path.join(DOWNLOADS_DIR, CREATED_IMAGE)
EXPECTED_CSS = os.path.join(DOWNLOADS_DIR, CREATED_CSS)
EXPECTED_JS = os.path.join(DOWNLOADS_DIR, CREATED_JS)


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


def test_folder_creation():
    folder = create_folder(URL, DOWNLOADS_DIR)
    assert os.path.join(DOWNLOADS_DIR, folder) == os.path.join(DOWNLOADS_DIR,
                                                               CREATED_DIR_NAME)


@pytest.mark.parametrize('expected', [
    CHANGED_HTML_FILE_NAME,
    CREATED_DIR_NAME,
    # CREATED_IMAGE,
    # CREATED_CSS,
    # CREATED_JS
])
def test_download_content(expected):
    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(URL, content=read_file(CREATED_HTML_FILE))
        mock.get(URL_IMAGE, content=read_file(EXPECTED_IMAGE))
        mock.get(URL_CSS, content=read_file(EXPECTED_CSS))
        mock.get(URL_JS, content=read_file(EXPECTED_JS))
        with tempfile.TemporaryDirectory() as directory:
            download(URL, directory)
            expected_path = os.path.join(directory, expected)
            assert os.path.exists(expected_path)


@pytest.mark.parametrize('new_file, old_file', [
    (CHANGED_HTML_FILE_NAME, HTML_FILE_NAME),
])
def test_change_html_file(new_file, old_file):
    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(URL, content=read_file(CREATED_HTML_FILE))
        with tempfile.TemporaryDirectory() as directory:
            download(URL, directory)
            new_file = os.path.join(directory, new_file)
            assert read_file(new_file) != read_file(old_file)


def test_get_html_file():
    result = get_html_file(URL, PATH_ORIGINAL)
    assert result == HTML_FILE_NAME


def test_get_content():
    try:
        get_content(URL)
    except Exception as exc:
        pytest.fail(exc, pytrace=True)
