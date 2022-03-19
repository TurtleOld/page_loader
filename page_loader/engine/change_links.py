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
    url_netloc = urlparse(link).netloc
    if urlparse(url).netloc == urlparse(link).netloc:
        return True
    if f'.{link_netloc}' == url_netloc:
        return True
    if not url_netloc:
        return True
    return False


def get_links_for_download(url, soup_data):
    domain_name = urlparse(url).netloc

    def get_link_to_file(search_tag, attribute):

        tags = soup_data.find_all(search_tag)

        for tag in tags:
            try:
                link = tag[attribute]
                print(link)
                if is_same_domain(link, domain_name):
                    print(link)
                    list_links_for_download.append((link, search_tag,
                                                    attribute))
            except KeyError:
                logger_error.error('The link is not downloaded because page '
                                   'loader '
                                   'does not support empty attributes')

    list_links_for_download = []

    for tag, attr in TAGS_ATTRIBUTES.items():
        get_link_to_file(tag, attr)
    return set(list_links_for_download)


def change_links(soup_data, search_tag, attribute, old_link, new_link):
    tags = soup_data.find_all(search_tag)

    for tag in tags:
        if tag[attribute] == old_link:
            tag[attribute] = new_link
