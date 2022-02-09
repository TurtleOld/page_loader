import logging
import os

from page_loader.engine.download_content import get_html_file, download_content

log = logging.getLogger(__name__)

CURRENT_DIRECTORY = os.getcwd()


def download(url, path=CURRENT_DIRECTORY):
    file_with_content = get_html_file(url, path)
    download_content(url, path)
    return file_with_content
