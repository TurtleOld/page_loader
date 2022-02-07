import os
import re

import requests
import tldextract
from bs4 import BeautifulSoup

TAGS_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href'
}


def get_new_link_format(url):
    link_without_protocol = re.sub(r'^(http|https)://', '', url)
    if link_without_protocol.endswith('/'):
        return re.sub(r'\W', '-', link_without_protocol[:-1])
    return re.sub(r'\W', '-', link_without_protocol)


def create_folder(url, path):
    string = get_new_link_format(url)
    folder_name = f'{string}_files'
    full_path = os.path.join(path, folder_name)

    if not os.path.isdir(full_path):
        os.mkdir(full_path)

    return folder_name


def get_domain_suite(url):
    domain = tldextract.extract(url)

    return f'{get_new_link_format(domain.subdomain)}-{domain.domain}-' \
           f'{domain.suffix}'


def save_to_file(path_to_file, data):
    if isinstance(data, bytes):
        with open(path_to_file, 'wb') as file_name:
            file_name.write(data)
    else:
        with open(path_to_file, 'w', encoding='utf-8') as file_name:
            file_name.write(data)


def get_content(url, path):
    try:
        response = requests.get(url)
        new_link = get_new_link_format(url)
        file_name = f'{new_link}.html'
        path_to_file = os.path.join(path, file_name)
        if response.status_code == 200:
            save_to_file(path_to_file, response.text)
            return path_to_file
    except requests.exceptions.HTTPError as Error:
        raise SystemExit(Error)


def download_content(url, path):
    file_content = get_content(url, path)

    def get_link_to_file(search_tag, attribute):

        tags = soup.find_all(search_tag)
        domain_name = get_domain_suite(url)
        folder_name = create_folder(url, path)

        for tag in tags:
            try:
                if tag[attribute].startswith('/') and \
                        not tag[attribute].startswith('//')\
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
