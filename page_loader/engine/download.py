import logging
import os

from page_loader.engine.download_content import get_html_file, \
    download_content, change_links

log = logging.getLogger(__name__)

CURRENT_DIRECTORY = os.getcwd()


def download(url, path=CURRENT_DIRECTORY):
    try:
        file_with_content = get_html_file(url, path)
        download_content(url, path)
        change_links(url, path)
    except FileNotFoundError:
        log.error(f'No such directory: {path}')
        raise 
    except IOError:
        log.error(f'No such directory: {path}')
        raise
    except TypeError:
        pass
    else:
        return file_with_content
