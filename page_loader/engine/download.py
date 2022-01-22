import os
import re

import requests

CURRENT_DIRECTORY = os.getcwd()


def download(url, path=CURRENT_DIRECTORY):
    link = url.replace('https://', '')
    new_link = re.sub('\W', '-', link)
    file_name = f'{new_link}.html'
    request_link = requests.get(url)
    with open(os.path.join(path, file_name), 'w',
              encoding='utf-8') as result_file:
        result_file.write(request_link.text)

        return result_file.name
