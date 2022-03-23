import os

import requests

from page_loader.engine.logger_config import logger_error, logger


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
        logger_error.error(f'Failed to establish a connection to site: {url}\n'
                           f'Response timeout expired')
        raise requests.exceptions.ConnectionError(
            f'Failed to establish a connection to site: {url}\n'
            f'Response timeout expired'
        )

    except requests.exceptions.TooManyRedirects:
        logger_error.error(f'Failed to establish a connection to site: {url}\n'
                           f'Too many redirects')
        raise requests.exceptions.TooManyRedirects(
            f'Failed to establish a connection to site: {url}\n'
            f'Too many redirects'
        )
    except requests.exceptions.HTTPError:
        logger_error.error(f'Failed to establish a connection to site: {url}\n'
                           f'HTTP Error occurred')
        raise requests.exceptions.HTTPError(
            f'Failed to establish a connection to site: {url}\n'
            f'HTTP Error occurred'
        )
    except requests.exceptions.ConnectionError:
        logger_error.error(f'Failed to establish a connection to site: {url}\n'
                           f'Please check your a connection to Ethernet '
                           f'or address site')
        raise requests.exceptions.ConnectionError(
            f'Failed to establish a connection to site: {url}\n'
            f'Please check your a connection to Ethernet or address site'
        )
    except requests.exceptions.RequestException:
        logger_error.error(f'Failed to establish a connection to site: {url}\n'
                           f'Other request exceptions occurred')
        raise requests.exceptions.RequestException(
            f'Failed to establish a connection to site: {url}\n'
            f'Other request exceptions occurred'
        )
    else:
        return response.content


def save_to_file(path_to_file, data):
    """
    A function that allows you to save files in bytes and regular.
    :param path_to_file: Path to file.
    :param data: File Contents.
    """
    format_file = 'w'
    if isinstance(data, bytes):
        format_file = 'wb'
    with open(path_to_file, format_file) as file_name:
        file_name.write(data)
    logger.info(f'Link {os.path.basename(file_name.name)} is downloaded')
