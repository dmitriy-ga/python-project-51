import argparse
import os
from src.page_loader import download
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
    except Exception:
        logging.error('Unable download page')
        sys.exit(1)


if __name__ == '__main__':
    main()
