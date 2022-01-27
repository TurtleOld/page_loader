import os
import re

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


def prepare(url) -> list[tuple]:
    soup = soup_parser(url)
    tags = soup.find_all('img')
    result = []
    for tag in tags:
        links = parse_tags(url, tag)
        result.append(links)
    print(result)
    return result


def download_images(url, path) -> list:
    folder_name = create_folder(url, path)
    links = prepare(url)
    result = []
    for link in links:
        if link[0].startswith('/'):
            with open(os.path.join(path, folder_name, link[1]), 'wb') as file_name:
                file_name.write(requests.get(f'{url}{link[0]}').content)
                result.append(os.path.join(folder_name, link[1]))
        else:
            with open(os.path.join(path, folder_name, link[1]), 'wb') as file_name:
                file_name.write(requests.get(link[0]).content)
                result.append(os.path.join(folder_name, link[1]))
    print(result)
    return result
