from bs4 import BeautifulSoup


def change_links(name_file, links):
    with open(name_file.name, 'r', encoding='utf-8') as file_path:
        soup = BeautifulSoup(file_path, 'html.parser')
        for tag in soup.find_all('img'):
            tag['src'] = links
        with open(name_file.name, 'w', encoding='utf-8') as new_file_path:
            new_file_path.write(str(soup))
