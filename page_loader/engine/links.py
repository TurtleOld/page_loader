from urllib.parse import urlparse

from page_loader.engine.logger_config import logger_error

TAGS_ATTRIBUTES = {
    'img': 'src',
    'script': 'src',
    'link': 'href',
}


def is_same_domain(link, url):
    if not link:
        return False
    link_netloc = urlparse(link).netloc
    url_netloc = urlparse(url).netloc
    if link_netloc == url_netloc or f'.{link_netloc}' == url_netloc \
            or not link_netloc:
        return True
    return False


def get_links_for_download(url, soup_data):

    list_links_for_download = []

    for tag, attribute in TAGS_ATTRIBUTES.items():
        for tag_soup in soup_data.find_all(tag):
            try:
                link = tag_soup[attribute]
                if is_same_domain(link, url):
                    list_links_for_download.append((link, tag_soup, attribute))
            except KeyError:
                logger_error.error('The link is not downloaded because page '
                                   'loader '
                                   'does not support empty attributes')

    return set(list_links_for_download)


def change_link(tag, attribute, resource_path_to_file):
    tag[attribute] = resource_path_to_file
