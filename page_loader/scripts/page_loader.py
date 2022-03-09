# ! /usr/bin/env python

import logging.config
import sys

from page_loader import download
from page_loader.engine.parse_cli_args import parse_cli_arguments

log = logging.getLogger(__name__)

LOG_FORMAT = '%(message)s'

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=LOG_FORMAT)


def main():
    try:
        args = parse_cli_arguments()
        file_path = download(args.url, args.output)
        if file_path is None:
            return
        print(f"Page was successfully downloaded into '{file_path}'")
        sys.exit(0)
    except Exception as error:
        log.error(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
