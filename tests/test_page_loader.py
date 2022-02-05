import os
import tempfile

from page_loader.engine.download_content import create_folder

URL = 'https://page-loader.hexlet.repl.co/'
template_dir = tempfile.TemporaryDirectory().name
# file_name = download(URL, template_dir)
# file_name_tests = download(URL, 'tests/fixtures')
# links = download_images(URL, 'tests/fixtures')
downloads_dir = os.path.join('tests', 'fixtures', 'downloads')
created_dir = os.path.join(downloads_dir,
                           'page-loader-hexlet-repl-co_files')
# created_html_file = os.path.join(template_dir,
#                                  'page-loader-hexlet-repl-co.html')


def test_folder_creation():
    folder = create_folder(URL, downloads_dir)
    assert folder == created_dir
