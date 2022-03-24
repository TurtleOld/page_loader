from urllib.parse import urlparse

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
    # def get_link_to_file(search_tag, attribute):

    #     tags = soup_data.find_all(search_tag)

    #     for tag in tags:
    #         try:
    #             link = tag[attribute]
    #             if is_same_domain(link, url):
    #                 list_links_for_download.append((link, search_tag,
    #                                                 attribute))
    #         except KeyError:
    #             logger_error.error('The link is not downloaded because page '
    #                                'loader '
    #                                'does not support empty attributes')

    list_links_for_download = []
    for tag, attribute in TAGS_ATTRIBUTES.items():
        for tag_soup in soup_data.find_all(tag):
            link = tag_soup[attribute]
            list_links_for_download.append((link, tag_soup, attribute))

    return set(list_links_for_download)
    # list_links_for_download = []

    # for tag, attr in TAGS_ATTRIBUTES.items():
    #     get_link_to_file(tag, attr)
    # return set(list_links_for_download)


def change_links(soup_data, attribute, resource_path_to_file):
    tags = soup_data.find_all(TAGS_ATTRIBUTES.keys())
    for tag in tags:
        tag[attribute] = resource_path_to_file
