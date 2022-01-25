import os
import re

import requests
from bs4 import BeautifulSoup


def get_new_link_format(url):
    link_without_protocol = re.sub(r'^(http|https)://', '', url)
    return re.sub(r'\W', '-', link_without_protocol)


def download_images(url, path=os.getcwd()):
    string = get_new_link_format(url)
    folder_name = f'{string}_files'
    full_path = os.path.join(path, folder_name)

    if not os.path.isdir(full_path):
        os.mkdir(full_path)

    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.content, 'html.parser')
    for tag in soup.find_all('img'):
        link_img = tag['src']
        path_name = get_new_link_format(os.path.dirname(tag['src']))
        file_name = f'{path_name}-{os.path.basename(link_img)}'
        with open(os.path.join(path, folder_name, file_name), 'wb') as \
                full_path_name:
            full_path_name.write(requests.get(f'{url}{link_img}').content)
            return os.path.join(folder_name, file_name)
