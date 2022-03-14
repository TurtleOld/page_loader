import os
import re
from pathlib import Path
from time import sleep
from urllib.parse import urlparse

from progress.bar import ChargingBar

from page_loader.engine.dicts import TAGS_ATTRIBUTES
from page_loader.engine.tools import create_folder
from page_loader.engine.tools import get_content
from page_loader.engine.tools import get_new_link_format
from page_loader.engine.tools import get_soup
from page_loader.engine.tools import save_to_file


def download_content(url, path):
    folder_name = create_folder(url, path)
    preparation = urlparse(url)
    domain_name = get_new_link_format(preparation.netloc)
    urls = f'{preparation.scheme}://{preparation.netloc}'

    def save_content_to_file(search_tag, attribute):

        tags = content_soup.find_all(search_tag)
        bar = ChargingBar('Loading', max=len(tags),
                          fill='#', suffix='%(percent)d%%')

        for tag in tags:
            file_name = f'{os.path.basename(tag[attribute])}'
            root_folder_to_file = os.path.dirname(tag[attribute])
            extension = Path(f'{urls}{tag[attribute]}').suffix
            match_by_extension = re.search(r'.\D{2,4}$', extension)

            if not tag[attribute].startswith('http'):

                if match_by_extension:
                    save_to_file(os.path.join(
                        path, folder_name,
                        f'{domain_name}'
                        f'{get_new_link_format(root_folder_to_file)}-'
                        f'{file_name}'),
                        get_content(f'{urls}{tag[attribute]}'))
                    bar.next()
                    sleep(1)

                else:
                    save_to_file(os.path.join(
                        path, folder_name,
                        f'{domain_name}'
                        f'{get_new_link_format(tag[attribute])}.html'
                    ),
                        get_content(f'{urls}{tag[attribute]}'))
                    bar.next()
                    sleep(1)

            if tag[attribute].startswith('http') \
                    and urlparse(url).netloc == urlparse(tag[attribute]).netloc:

                if match_by_extension:
                    save_to_file(os.path.join(
                        path, folder_name,
                        f'{get_new_link_format(root_folder_to_file)}-'
                        f'{file_name}'),
                        get_content(tag[attribute]))
                    bar.next()
                    sleep(1)

                else:
                    save_to_file(os.path.join(
                        path, folder_name,
                        f'{domain_name}'
                        f'{get_new_link_format(root_folder_to_file)}-'
                        f'{get_new_link_format(tag[attribute])}.html'
                    ),
                        get_content(tag[attribute]))
                    bar.next()
                    sleep(1)

            bar.finish()

    content_soup = get_soup(url)

    for tag_name, attr in TAGS_ATTRIBUTES.items():
        save_content_to_file(tag_name, attr)
