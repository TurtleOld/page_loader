import os

from page_loader.engine.services import get_content, save_to_file
from page_loader.engine.url import get_file_name


def download_content(url, path):
    file_name = get_file_name(url)
    file_path = os.path.join(path, file_name)
    content = get_content(url)
    save_to_file(file_path, content)
    return file_name
