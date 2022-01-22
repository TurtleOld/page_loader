import os
import tempfile

import requests
from requests_mock.mocker import Mocker

link = 'https://ru.hexlet.io/courses'
new_link = link.replace('https://', '').replace('.', '-').replace('/', '-')
file_name = f'{new_link}.html'
html = requests.get(link)


def test_page_loader(requests_mock: Mocker):
    temp_dir = tempfile.TemporaryDirectory()
    with open(os.path.join(temp_dir.name, file_name), 'w') as file1:
        file1.write(html.text)
        with open(file1.name, 'r') as file2:
            data = file2.read()
            requests_mock.get(link, text=data)
            assert data == requests.get(link).text
