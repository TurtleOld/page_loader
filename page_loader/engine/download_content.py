import os
import re

import requests
from bs4 import BeautifulSoup


def get_link_without_protocol(url):
    return re.sub(r'^(http|https)://', '', url)


def download_images(url, path=os.getcwd()):
    link_without_protocol = get_link_without_protocol(url)
    string = re.sub(r'\W', '-', link_without_protocol)
    folder_name = f'{string}_files'
    full_path = os.path.join(path, folder_name)

    if not os.path.isdir(full_path):
        os.mkdir(full_path)

    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.content, 'html.parser')
    for tag in soup.find_all('img'):
        link_img_without_protocol = get_link_without_protocol(tag['src'])
        link_img = tag['src']
        path_name = re.sub(r'\W', '-',
                           os.path.dirname(link_img_without_protocol))
        file_name = f'{path_name}-{os.path.basename(link_img_without_protocol)}'
        with open(os.path.join(path, folder_name, file_name), 'wb') as \
                full_path_name:
            full_path_name.write(requests.get(f'{url}{link_img}').content)
            return os.path.join(folder_name, file_name)
