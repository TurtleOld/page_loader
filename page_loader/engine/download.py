import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from progress.bar import PixelBar

from page_loader.engine.download_content import download_content
from page_loader.engine.links import change_link, get_links_for_download
from page_loader.engine.logger_config import logger, logger_error
from page_loader.engine.services import get_content
from page_loader.engine.services import save_to_file
from page_loader.engine.url import get_new_name_link, get_name_folder


def download(url, path):
    content = get_content(url)
    soup_data = BeautifulSoup(content, 'html.parser')
    main_file_name = os.path.join(path, get_new_name_link(url) + '.html')
    folder_name = get_name_folder(url)
    folder_for_download = os.path.join(path, folder_name)
    if not os.path.isdir(folder_for_download):
        os.mkdir(folder_for_download)
        logger.info(f'Folder {folder_for_download} created\n')
    else:
        logger.info(f'Folder {folder_for_download} exists\n')

    links_for_download = get_links_for_download(url, soup_data)

    bar = PixelBar(max=len(links_for_download),
                   suffix='%(percent)d%%\n\n')

    for link, search_tag, attribute in links_for_download:
        try:

            new_link = urljoin(url, link)

            resource_file_name = download_content(new_link,
                                                  folder_for_download)
            resource_folder_name = os.path.basename(folder_for_download)
            resource_path_to_file = os.path.join(resource_folder_name,
                                                 resource_file_name)
            change_link(search_tag, attribute, resource_path_to_file)

            bar.next()
        except requests.exceptions.Timeout as timeout_error:
            logger_error.warning(timeout_error)
        except requests.exceptions.HTTPError as http_error:
            logger_error.warning(http_error)
        except requests.exceptions.ConnectionError as conn_error:
            logger_error.warning(conn_error)

    bar.finish()

    soup_data = soup_data.prettify()
    save_to_file(main_file_name, soup_data)

    return main_file_name
