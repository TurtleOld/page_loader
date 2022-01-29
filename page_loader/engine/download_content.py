import os
import re
from typing import Any

import requests
import tldextract
from bs4 import BeautifulSoup
from bs4.element import Tag


def get_new_link_format(url):
    link_without_protocol = re.sub(r'^(http|https)://', '', url)
    return re.sub(r'\W', '-', link_without_protocol)


def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(response.status_code)


def soup_parser(url):
    html = get_content(url)
    return BeautifulSoup(html, 'html.parser')


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


def parse_tags(url: str, tag: Tag):
    tags_url = tag['src']
    domain_name = get_domain_suite(url)
    path_name = get_new_link_format(os.path.dirname(tags_url))
    file_name = f'{domain_name}-{path_name}-{os.path.basename(tags_url)}'
    return tags_url, file_name


def prepare(url) -> tuple[list[tuple[Any, str]], list[Any]]:
    soup = soup_parser(url)
    tags = soup.find_all('img')
    list_links = []
    list_tags = []
    for tag in tags:
        links = parse_tags(url, tag)
        list_links.append(links)
        list_tags.append(tag)
    return list_links, list_tags


def download_images(url, path) -> dict[tuple[Any, str], str]:
    folder_name = create_folder(url, path)
    links = prepare(url)
    list_links, list_tags = links
    result = []
    for link in list_links:
        if link[0].startswith('/'):
            with open(os.path.join(path, folder_name, link[1]),
                      'wb') as file_name:
                file_name.write(requests.get(f'{url}{link[0]}').content)
                result.append(os.path.join(folder_name, link[1]))
        else:
            with open(os.path.join(path, folder_name, link[1]),
                      'wb') as file_name:
                file_name.write(requests.get(link[0]).content)
                result.append(os.path.join(folder_name, link[1]))

    return dict(zip(list_tags, result))
