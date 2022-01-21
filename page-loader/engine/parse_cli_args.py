import argparse

DESCRIPTION = 'Internet page loader'
OUTPUT_FLAG_1 = '-o'
OUTPUT_FLAG_2 = '--output'
FORMAT_HELP = 'output dir (default "/app")'
VERSION_STRING_1 = '-v'
VERSION_STRING_2 = '--version'
VERSION_NUMBER = '{0} 1.0'.format(DESCRIPTION)


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    args = parser.parse_args()
    return args
