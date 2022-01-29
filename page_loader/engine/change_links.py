from bs4 import BeautifulSoup


def change_links(file_path, links):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        tags = soup.find_all('img')
    for key, value in links.items():
        key['src'] = value
        print(key)
