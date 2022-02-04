import os
import re

import requests
import tldextract
from bs4 import BeautifulSoup
from bs4.element import Tag


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
    return f'{domain.subdomain}-{domain.domain}-{domain.suffix}'


def save_to_file(path_to_file, data):
    if isinstance(data, bytes):
        with open(path_to_file, 'wb') as file_name:
            file_name.write(data)
    else:
        with open(path_to_file, 'w', encoding='utf-8') as file_name:
            file_name.write(data)


def get_content(url, path):
    response = requests.get(url)
    new_link = get_new_link_format(url)
    file_name = f'{new_link}.html'
    path_to_file = os.path.join(path, file_name)
    if response.status_code == 200:
        save_to_file(path_to_file, response.text)
        return path_to_file
    else:
        print(response.status_code)


def parse_tags(url: str, tag: Tag):
    tags_url = tag['src']
    domain_name = get_domain_suite(url)
    path_name = get_new_link_format(os.path.dirname(tags_url))
    file_name = f'{domain_name}-{path_name}-{os.path.basename(tags_url)}'
    return tags_url, file_name


def download_images(url, path):
    file_content = get_content(url, path)
    folder_name = create_folder(url, path)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('img')
    list_links = []
    list_path_to_images = []

    for tag in tags:
        links = parse_tags(url, tag)
        list_links.append(links)
    for link in list_links:
        if link[0].startswith('/'):
            save_to_file(os.path.join(path, folder_name, link[1]),
                         requests.get(f'{url}{link[0]}').content)

            list_path_to_images.append(os.path.join(folder_name, link[1]))
        else:
            save_to_file(os.path.join(path, folder_name, link[1]),
                         requests.get(link[0]).content)

            list_path_to_images.append(os.path.join(folder_name, link[1]))

    tuple_tags_links = dict(zip(tags, list_path_to_images))

    for key, value in tuple_tags_links.items():
        key['src'] = value

    save_to_file(file_content, soup.prettify(formatter='html5'))
