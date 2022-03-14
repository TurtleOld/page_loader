import os
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from page_loader.engine.logging_config import log


def get_new_link_format(url) -> str:
    """
    Function to change the presentation of the site link.
    :param url: Link to the website.
    :return: Prepared site link.
    """
    link_preparation = urlparse(url)
    new_link = re.sub(r'\W', '-', f'{link_preparation.netloc}'
                                  f'{link_preparation.path}')
    return new_link


def create_folder(url, path) -> str:
    """
    Folder creation function.
    :param url: Link to the website.
    :param path: The path to save the content.
    :return: Name of the created folder.
    """
    domain_name = get_new_link_format(url)
    folder_name = f'{domain_name}_files'
    full_path = os.path.join(path, folder_name)

    if not os.path.isdir(full_path):
        try:
            os.mkdir(full_path)
        except PermissionError:
            log.error(f'Permission denied to the specified directory:'
                      f' {path}')
            raise PermissionError(
                f'Permission denied to the specified directory:'
                f' {path}')
        except OSError:
            log.error(f'Failed to create folder {folder_name}')
            raise OSError(f'Failed to create folder {folder_name}')

    return folder_name


def save_to_file(path_to_file, data):
    """
    A function that allows you to save files in bytes and regular.
    :param path_to_file: Path to file.
    :param data: File Contents.
    """
    if isinstance(data, bytes):
        with open(path_to_file, 'wb') as file_name:
            file_name.write(data)

    else:
        with open(path_to_file, 'w', encoding='utf-8') as file_name:
            file_name.write(data)


def get_html_file_with_content(url, path):
    """
    The function of creating an html file and writing content to this file.
    :param url: Link to the website.
    :param path: The path to save the content.
    :return: The path to file
    """
    file_content = get_content(url)

    if file_content:
        new_link = get_new_link_format(url)
        file_name = f'{new_link}.html'
        path_to_file = os.path.join(path, file_name)
        save_to_file(path_to_file, file_content)

        return path_to_file


def get_content(url):
    """
    The function for receiving the content of the Internet page.
    :param url: Link to the website.
    :return: Content of the Internet page.
    """
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
    except requests.exceptions.ConnectTimeout:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Response timeout expired')
        raise requests.exceptions.ConnectionError(
            f'Failed to establish a connection to site: {url}\n'
            f'Response timeout expired'
        )

    except requests.exceptions.TooManyRedirects:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Too many redirects')
        raise requests.exceptions.TooManyRedirects(
            f'Failed to establish a connection to site: {url}\n'
            f'Too many redirects'
        )
    except requests.exceptions.HTTPError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'HTTP Error occurred')
        raise requests.exceptions.HTTPError(
            f'Failed to establish a connection to site: {url}\n'
            f'HTTP Error occurred'
        )
    except requests.exceptions.ConnectionError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Please check your a connection to Ethernet')
        raise requests.exceptions.ConnectionError(
            f'Failed to establish a connection to site: {url}\n'
            f'Please check your a connection to Ethernet'
        )
    except requests.exceptions.RequestException:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Other request exceptions occurred')
        raise requests.exceptions.RequestException(
            f'Failed to establish a connection to site: {url}\n'
            f'Other request exceptions occurred'
        )
    else:
        return response.content


def get_soup(url):
    """
    Function for preparing file content using the BeautifulSoup library.
    :param url: Link to the website.
    :return: File Contents
    """
    content = get_content(url)
    return BeautifulSoup(content, 'html.parser')
