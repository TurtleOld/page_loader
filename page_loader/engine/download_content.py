import logging
import os
import re
import socket
from urllib.parse import urlparse

import requests
import urllib3.exceptions
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

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
            raise

    return folder_name


def save_to_file(path_to_file, data):
    try:
        if isinstance(data, bytes):
            with open(path_to_file, 'wb') as file_name:
                file_name.write(data)
        else:
            with open(path_to_file, 'w', encoding='utf-8') as file_name:
                file_name.write(data)
    except PermissionError:
        log.error(f'Permission denied to the specified directory '
                  f'{path_to_file}')


def get_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
    except urllib3.exceptions.MaxRetryError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
    except urllib3.exceptions.NewConnectionError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
    except urllib3.exceptions.HTTPError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
    except socket.gaierror:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link! ')
        raise
    else:
        return response.content


def get_html_file(url, path):

    response = get_content(url)

    if response:
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
        result = []

        for tag in tags:
            try:

                if tag[attribute].startswith('/') and \
                        not tag[attribute].startswith('//') \
                        and tag[attr].endswith(('png', 'jpg', 'js', 'css')):
                    result.append(tag)

            except KeyError:
                continue

        bar = IncrementalBar('Download', max=len(result),
                             suffix='%(percent).1f%%')
        for tg in result:
            bar.next()
            path_name = \
                get_new_link_format(os.path.dirname(tg[attribute]))
            file_name = f'{domain_name}-{path_name}-' \
                        f'{os.path.basename(tg[attribute])}'

            save_to_file(os.path.join(path, folder_name, file_name),
                         requests.get(f'{url}{tg[attribute]}').content)

            tg[attribute] = os.path.join(folder_name, file_name)

        bar.finish()

    response = get_content(url)
    soup = BeautifulSoup(response, 'html.parser')

    for tag_name, attr in TAGS_ATTRIBUTES.items():
        get_link_to_file(tag_name, attr)

    save_to_file(file_content, soup.prettify(formatter='minimal'))
