import os

from page_loader.engine.logger_config import logger


def save_to_file(path_to_file, data):
    """
    A function that allows you to save files in bytes and regular.
    :param path_to_file: Path to file.
    :param data: File Contents.
    """
    format_file = 'w'
    if isinstance(data, bytes):
        format_file = 'wb'
    with open(path_to_file, format_file) as file_name:
        file_name.write(data)
    logger.info(f'Link {os.path.basename(file_name.name)} is downloaded')