import argparse
import os

DESCRIPTION = 'Internet page loader'
OUTPUT_FLAG_1 = '-o'
OUTPUT_FLAG_2 = '--output'
OUTPUT_HELP = 'output dir (default "current directory")'
VERSION_STRING_1 = '-v'
VERSION_STRING_2 = '--version'
VERSION_NUMBER = f'{DESCRIPTION} 1.0'


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION,
                                     prog='page-loader',
                                     usage='%(prog)s [options] <url>')
    parser.add_argument(OUTPUT_FLAG_1, OUTPUT_FLAG_2,
                        help=OUTPUT_HELP,
                        default=os.getcwd())
    parser.add_argument('url', type=str)
    parser.add_argument(VERSION_STRING_1, VERSION_STRING_2,
                        version=VERSION_NUMBER, action='version')
    args = parser.parse_args()
    return args
