import os
import re
from pathlib import Path
from urllib.parse import urlparse

from page_loader.engine.dicts import TAGS_ATTRIBUTES
from page_loader.engine.tools import create_folder
from page_loader.engine.tools import get_html_file_with_content
from page_loader.engine.tools import get_new_link_format
from page_loader.engine.tools import get_soup
from page_loader.engine.tools import save_to_file


def change_links(url, path):
    """
    Function for changing links and writing them to a file
    :param url: Link to the website.
    :param path: The path to save the content.
    """
    path_to_file = get_html_file_with_content(url, path)
    link_preparation = urlparse(url)
    domain_name = get_new_link_format(link_preparation.netloc)
    urls = f'{link_preparation.scheme}://{link_preparation.netloc}'
    folder_name = create_folder(url, path)

    def get_link_to_file(search_tag, attribute):

        tags = content_soup.find_all(search_tag)

        for tag in tags:
            file_name = f'{os.path.basename(tag[attribute])}'
            root_folder_to_file = os.path.dirname(tag[attribute])
            extension = Path(f'{urls}{tag[attribute]}').suffix
            match_by_extension = re.search(r'.\D{2,4}$', extension)

            if not tag[attribute].startswith('http'):

                if match_by_extension:
                    tag[attribute] = os.path.join(
                        folder_name,
                        f'{domain_name}'
                        f'{get_new_link_format(root_folder_to_file)}-'
                        f'{file_name}')
                else:
                    tag[attribute] = os.path.join(
                        folder_name,
                        f'{domain_name}'
                        f'{get_new_link_format(root_folder_to_file)}'
                        f'{file_name}.html')

            if tag[attribute].startswith('http') \
                    and urlparse(url).netloc == urlparse(tag[attribute]).netloc:
                if match_by_extension:
                    tag[attribute] = os.path.join(
                        folder_name,
                        f'{get_new_link_format(root_folder_to_file)}-'
                        f'{file_name}')
                else:
                    tag[attribute] = os.path.join(
                        folder_name,
                        f'{domain_name}'
                        f'{get_new_link_format(root_folder_to_file)}-'
                        f'{file_name}.html')

    content_soup = get_soup(url)

    for tag_name, attr in TAGS_ATTRIBUTES.items():
        get_link_to_file(tag_name, attr)

    save_to_file(path_to_file, content_soup.prettify(formatter='minimal'))
