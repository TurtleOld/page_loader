import os

import pytest
from requests.exceptions import HTTPError, ConnectionError, \
    RequestException, TooManyRedirects, ConnectTimeout

from page_loader import download

URL = 'https://page-loader.hexlet.repl.co'
TEST_FOLDER = os.path.dirname(__file__)
INTERNET_PATH_IMAGE = '/assets/professions/nodejs.png'
INTERNET_PATH_CSS = '/assets/application.css'
INTERNET_PATH_JS = '/script.js'
INTERNET_PATH_FILE = '/courses'
URL_IMAGE = os.path.join(URL, INTERNET_PATH_IMAGE)
URL_CSS = os.path.join(URL, INTERNET_PATH_CSS)
URL_JS = os.path.join(URL, INTERNET_PATH_JS)
URL_FILE = os.path.join(URL, INTERNET_PATH_FILE)

PATH_ORIGINAL = os.path.join(TEST_FOLDER, 'fixtures', 'downloads')
DOWNLOADS_DIR = os.path.join(TEST_FOLDER, 'fixtures', 'downloads', 'changed')

HTML_FILE_NAME = os.path.join(PATH_ORIGINAL, 'page-loader-hexlet-repl-co.html')
CHANGED_HTML_FILE_NAME = 'page-loader-hexlet-repl-co.html'
CREATED_DIR_NAME = 'page-loader-hexlet-repl-co_files'
IMAGE_NAME = 'page-loader-hexlet-repl-co-assets-professions-nodejs.png'
CSS_NAME = 'page-loader-hexlet-repl-co-assets-application.css'
JS_NAME = 'page-loader-hexlet-repl-co-script.js'
FILE_NAME = 'page-loader-hexlet-repl-co-courses.html'

CREATED_HTML_FILE = os.path.join(DOWNLOADS_DIR, CHANGED_HTML_FILE_NAME)
CREATED_IMAGE = os.path.join(CREATED_DIR_NAME, IMAGE_NAME).strip()
CREATED_CSS = os.path.join(CREATED_DIR_NAME, CSS_NAME).strip()
CREATED_JS = os.path.join(CREATED_DIR_NAME, JS_NAME).strip()
CREATED_FILE = os.path.join(CREATED_DIR_NAME, FILE_NAME).strip()

EXPECTED_IMAGE = os.path.join(DOWNLOADS_DIR, CREATED_IMAGE).strip()
EXPECTED_DIR = os.path.join(DOWNLOADS_DIR, CREATED_DIR_NAME).strip()
EXPECTED_CSS = os.path.join(DOWNLOADS_DIR, CREATED_CSS).strip()
EXPECTED_JS = os.path.join(DOWNLOADS_DIR, CREATED_JS).strip()
EXPECTED_FILE = os.path.join(DOWNLOADS_DIR, CREATED_FILE).strip()


def read_file(file):
    with open(file, 'rb') as f:
        return f.read()


@pytest.mark.parametrize('new_file, expect_file', [
    (CHANGED_HTML_FILE_NAME, CREATED_HTML_FILE),
    (CREATED_IMAGE, EXPECTED_IMAGE),
    (CREATED_CSS, EXPECTED_CSS),
    (CREATED_JS, EXPECTED_JS),
])
def test_download_content(new_file, expect_file, tmpdir, requests_mock):
    requests_mock.get(URL, content=read_file(HTML_FILE_NAME))
    requests_mock.get(URL_IMAGE, content=read_file(EXPECTED_IMAGE))
    requests_mock.get(URL_CSS, content=read_file(EXPECTED_CSS))
    requests_mock.get(URL_JS, content=read_file(EXPECTED_JS))
    requests_mock.get(URL_FILE, content=read_file(EXPECTED_FILE))
    assert not os.listdir(tmpdir)
    download(URL, tmpdir)
    expected_path = os.path.join(tmpdir, new_file)
    new_file = os.path.join(tmpdir, new_file)
    assert read_file(new_file) == read_file(expect_file)
    assert len(
        os.listdir(os.path.join(tmpdir, CREATED_DIR_NAME))) == 4
    assert os.path.exists(expected_path)


expected = [
    (ConnectTimeout, f'Failed to establish a connection to site: {URL}\n'
                     f'Response timeout expired'),
    (HTTPError, f'Failed to establish a connection to site: {URL}\n'
                f'HTTP Error occurred'),
    (ConnectionError, f'Failed to establish a connection to site: {URL}\n'
                      f'Please check your a connection to Ethernet '
                      f'or address site'),
    (TooManyRedirects, f'Failed to establish a connection to site: {URL}\n'
                       f'Too many redirects'),
    (RequestException, f'Failed to establish a connection to site: {URL}\n'
                       f'Other request exceptions occurred'),
]


@pytest.mark.parametrize('connection_error_excepted, expected_value', expected)
def test_connection(connection_error_excepted, expected_value, tmpdir,
                    requests_mock):
    with pytest.raises(Exception) as error:
        requests_mock.get(URL, exc=connection_error_excepted)
        download(URL, tmpdir)
    assert str(error.value) == expected_value


def test_not_exist_folder():
    with pytest.raises(OSError) as err:
        directory = os.path.join(PATH_ORIGINAL, CREATED_DIR_NAME, 'not_exist')
        download(URL, directory)
    assert str(err)


def test_denied_to_folder(tmpdir, requests_mock):
    requests_mock.get(URL)
    os.chmod(tmpdir, 400)
    with pytest.raises(PermissionError) as error:
        download(URL, tmpdir)
    assert f'Permission denied to the specified directory: {tmpdir}' \
           == str(error.value)
