import os

from page_loader.engine.change_links import change_links
from page_loader.engine.download_content import download_content
from page_loader.engine.tools import get_html_file_with_content
from page_loader.engine.logging_config import log

CURRENT_DIRECTORY = os.getcwd()


def download(url, path=CURRENT_DIRECTORY):
    try:
        file_with_content = get_html_file_with_content(url, path)
        download_content(url, path)
        change_links(url, path)
    except FileNotFoundError:
        log.error(f'No such directory: {path}')
        raise FileNotFoundError(f'No such directory: {path}')
    else:
        return file_with_content
