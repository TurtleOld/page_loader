# ! /usr/bin/env python
from page_loader.engine.download import download
from page_loader.engine.parse_cli_args import parse_cli_arguments


def main():
    args = parse_cli_arguments()
    file_path = download(args.url, args.output)
    print(file_path)


if __name__ == '__main__':
    main()
