# ! /usr/bin/env python

from page_loader import download
from page_loader.engine.logger_config import logger_error
from page_loader.engine.parse_cli_args import parse_cli_arguments


def main():
    try:
        args = parse_cli_arguments()
        file_path = download(args.url, args.output)
        print(f"Page was successfully downloaded into '{file_path}'")

    except PermissionError as error:
        print(f'Permission denied to the specified directory: '
              f'{error.filename}')
        logger_error.error(f'Permission denied to the specified directory: '
                           f'{error.filename}')

    except FileNotFoundError as error2:
        print(f'The system cannot find the path specified: '
              f'{error2.filename}')
        logger_error.error(f'The system cannot find the path specified: '
                           f'{error2.filename}')

    except KeyError as key_error:
        print(str(key_error))

    except Exception as exception:
        print(str(exception))


if __name__ == '__main__':
    main()
