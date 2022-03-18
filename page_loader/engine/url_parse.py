import os
import re
from urllib.parse import urlparse


def get_new_name_link(url) -> str:
    """
    Function to change the presentation of the site link.
    :param url: Link to the website.
    :return: Prepared site link.
    """
    link_preparation = urlparse(url)
    new_link = re.sub(r'\W', '-', f'{link_preparation.netloc}'
                                  f'{link_preparation.path}')
    return new_link


def get_file_name(url):
    """
    Function for getting the file name.
    :param url: Link to the website.
    :return: Name file
    """
    parse_url = urlparse(url)
    path_to_file = ''.join([parse_url.netloc, parse_url.path])
    file_name, extension = os.path.splitext(path_to_file)
    file_name = get_new_name_link(file_name)
    if not extension:
        extension = '.html'
    return file_name + extension


def get_name_folder(url) -> str:
    """
    Function for getting the folder name.
    :param url: Link to the website.
    :return: Name folder.
    """
    domain_name = get_new_name_link(url)
    folder_name = f'{domain_name}_files'

    return folder_name


