import os
import re

import requests

from page_loader.engine.change_links import change_links
from page_loader.engine.download_content import download_images

CURRENT_DIRECTORY = os.getcwd()


def download(url, path=CURRENT_DIRECTORY):
    without_protocol = url.replace('https://', '')
    new_link = re.sub(r'\W', '-', without_protocol)
    file_name = f'{new_link}.html'
    request_link = requests.get(url)
    with open(os.path.join(path, file_name), 'w',
              encoding='utf-8') as result_file:
        result_file.write(request_link.text)
        links = download_images(url, path)
        change_links(result_file, links)

        return result_file.name
