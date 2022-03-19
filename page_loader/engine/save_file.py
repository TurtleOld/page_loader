import os

from page_loader.engine.logger_config import logger


def save_to_file(path_to_file, data):
    """
    A function that allows you to save files in bytes and regular.
    :param path_to_file: Path to file.
    :param data: File Contents.
    """
    if isinstance(data, bytes):
        with open(path_to_file, 'wb') as file_name:
            logger.info(f'Link {os.path.basename(file_name.name)} is '
                        f'downloaded')
            file_name.write(data)

    else:
        with open(path_to_file, 'w', encoding='utf-8') as file_name:
            logger.info(f'Link {os.path.basename(file_name.name)} is '
                        f'downloaded')
            file_name.write(data)
