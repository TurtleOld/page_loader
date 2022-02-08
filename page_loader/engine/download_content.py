import logging
import os
import re
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

TAGS_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href'
}

log = logging.getLogger(__name__)


def get_new_link_format(url):
    preparation = urlparse(url)
    new_link = re.sub(r'\W', '-', f'{preparation.netloc}{preparation.path}')
    return new_link


def create_folder(url, path):
    string = get_new_link_format(url)
    folder_name = f'{string}_files'
    full_path = os.path.join(path, folder_name)

    if not os.path.isdir(full_path):
        try:
            os.mkdir(full_path)
        except IOError:
            log.error(f'Failed to create folder {folder_name}')
            sys.exit(1)

    return folder_name


def save_to_file(path_to_file, data):
    if isinstance(data, bytes):
        with open(path_to_file, 'wb') as file_name:
            file_name.write(data)
    else:
        with open(path_to_file, 'w', encoding='utf-8') as file_name:
            file_name.write(data)


def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    except requests.exceptions.ConnectionError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        sys.exit(1)


def get_html_file(url, path):
    response = get_content(url)
    new_link = get_new_link_format(url)
    file_name = f'{new_link}.html'
    path_to_file = os.path.join(path, file_name)
    save_to_file(path_to_file, response)
    return path_to_file


def download_content(url, path):
    file_content = get_html_file(url, path)

    def get_link_to_file(search_tag, attribute):

        tags = soup.find_all(search_tag)
        domain_name = get_new_link_format(url)
        folder_name = create_folder(url, path)

        for tag in tags:
            try:
                log.info(f'Link download {url}{tag[attr]}')
                if tag[attribute].startswith('/') and \
                        not tag[attribute].startswith('//') \
                        and tag[attr].endswith(('png', 'jpg', 'js', 'css')):
                    path_name = \
                        get_new_link_format(os.path.dirname(tag[attribute]))
                    file_name = f'{domain_name}-{path_name}-' \
                                f'{os.path.basename(tag[attribute])}'

                    save_to_file(os.path.join(path, folder_name, file_name),
                                 requests.get(f'{url}{tag[attribute]}').content)

                    tag[attribute] = os.path.join(folder_name, file_name)
            except KeyError:
                continue

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for tag_name, attr in TAGS_ATTRIBUTES.items():
        get_link_to_file(tag_name, attr)

    save_to_file(file_content, soup.prettify(formatter='minimal'))
