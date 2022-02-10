import os
import tempfile

import pytest
import requests
from requests_mock import Mocker

from page_loader import download
from page_loader.engine.download_content import get_content

INVALID_URL = 'https://badsite.com'
URL = 'https://page-loader.hexlet.repl.co'


def test_connection_error(requests_mock: Mocker):

    requests_mock.get(INVALID_URL, exc=requests.exceptions.ConnectionError)

    with tempfile.TemporaryDirectory() as tmp_dir_name:
        assert not os.listdir(tmp_dir_name)

        with pytest.raises(Exception):
            assert download(INVALID_URL, tmp_dir_name)

        assert not os.listdir(tmp_dir_name)


def test_get_content():
    try:
        get_content(URL)
    except Exception as exc:
        assert pytest.fail(exc, pytrace=True)
