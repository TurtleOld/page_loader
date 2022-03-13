# ! /usr/bin/env python

import sys

from page_loader import download
from page_loader.engine.parse_cli_args import parse_cli_arguments


def main():
    try:
        args = parse_cli_arguments()
        file_path = download(args.url, args.output)
        if file_path is None:
            return
        print(f"Page was successfully downloaded into '{file_path}'")
        sys.exit(0)
    except Exception as error:
        str(error)
        sys.exit(1)


if __name__ == '__main__':
    main()
