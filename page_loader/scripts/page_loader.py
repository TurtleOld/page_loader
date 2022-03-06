# ! /usr/bin/env python

import logging.config
import sys

from page_loader import download
from page_loader.engine.parse_cli_args import parse_cli_arguments

log = logging.getLogger(__name__)

LOG_FORMAT = '%(message)s'

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)


def main():
    args = parse_cli_arguments()

    file_path = download(args.url, args.output)
    if file_path is None:
        return
    log.info(f"Page was successfully downloaded into '{file_path}'")


if __name__ == '__main__':
    main()
