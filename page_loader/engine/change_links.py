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


def get_links_for_download(soup_data):

    list_links_for_download = []

    for tag, attribute in TAGS_ATTRIBUTES.items():
        for tag_soup in soup_data.find_all(tag):
            link = tag_soup[attribute]
            list_links_for_download.append((link, tag_soup, attribute))

    return set(list_links_for_download)


def change_links(search_tag, attribute, resource_path_to_file):
    search_tag[attribute] = resource_path_to_file
