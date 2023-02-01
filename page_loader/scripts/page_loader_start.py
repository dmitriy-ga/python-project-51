import argparse
import os
from page_loader.page_loader import download
import logging
import sys


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Downloads webpage via URL.'
    )
    current_directory = os.getcwd()
    parser.add_argument('-o', '--output',
                        help='path to save the page',
                        default=current_directory)
    parser.add_argument('url')

    args = parser.parse_args()
    output = args.output
    url = args.url

    try:
        print(download(url, output))
    except Exception as error:
        logging.error(f'Unable download page: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()
