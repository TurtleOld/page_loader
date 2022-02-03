import os

from page_loader.engine.download_content import get_content, download_images

CURRENT_DIRECTORY = os.getcwd()


def download(url, path=CURRENT_DIRECTORY):
    file_with_content = get_content(url, path)
    download_images(url, path)

    return file_with_content
