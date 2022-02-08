# ! /usr/bin/env python

import logging.config
import sys

from page_loader.engine.download import download
from page_loader.engine.parse_cli_args import parse_cli_arguments

log = logging.getLogger(__name__)

LOG_FORMAT = '%(message)s'

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=LOG_FORMAT)


def main():
    args = parse_cli_arguments()
    try:
        file_path = download(args.url, args.output)
        log.info(f"Page was successfully downloaded into '{file_path}'")
    except FileNotFoundError:
        log.error(f'ERROR: No such directory: {args.output}')


if __name__ == '__main__':
    main()
