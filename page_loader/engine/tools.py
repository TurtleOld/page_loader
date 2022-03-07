import logging
import os
import re
import socket
from urllib.parse import urlparse

import requests
import urllib3
from bs4 import BeautifulSoup

log = logging.getLogger(__name__)


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
    if requests.get(url).status_code == 200:
        domain_name = get_new_link_format(url)
        folder_name = f'{domain_name}_files'
        full_path = os.path.join(path, folder_name)

        if not os.path.isdir(full_path):
            try:
                os.mkdir(full_path)
            except IOError:
                log.error(f'Failed to create folder {folder_name}')
                raise

        return folder_name


def save_to_file(path_to_file, data):
    """
    A function that allows you to save files in bytes and regular.
    :param path_to_file: Path to file.
    :param data: File Contents.
    """
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
        raise


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
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise requests.exceptions.HTTPError('An HTTP error occurred.')
    except requests.exceptions.SSLError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise requests.exceptions.SSLError('An SSL error occurred.')
    except requests.exceptions.ConnectionError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise requests.exceptions.ConnectionError(
            'A Connection error occurred.')
    except requests.RequestException:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise
    except urllib3.util.ssl_:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise
    except urllib3.exceptions.MaxRetryError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise urllib3.exceptions.MaxRetryError('Max retries exceeded with url')
    except urllib3.exceptions.NewConnectionError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise urllib3.exceptions.NewConnectionError('Fail to establish '
                                                    'a new connection.')
    except urllib3.exceptions.HTTPError:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link!')
        raise urllib3.exceptions.HTTPError('An HTTP error occurred.')
    except socket.gaierror:
        log.error(f'Failed to establish a connection to site: {url}\n'
                  f'Check the correctness of the entered link! ')
        raise socket.gaierror('Failed to execute script')
    else:
        return response.content


def get_soup(url):
    """
    Function for preparing file content using the BeautifulSoup library.
    :param url: Link to the website.
    :return: File Contents
    """
    file_content = get_content(url)
    return BeautifulSoup(file_content, 'html.parser')
