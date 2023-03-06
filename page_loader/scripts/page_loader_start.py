from page_loader.cli import parse_cli_args
from page_loader.page_loader import download
import logging
import sys


def main() -> None:
    args = parse_cli_args()
    output = args.output
    url = args.url

    try:
        print(download(url, output))
    except Exception as error:
        logging.error(f'Unable download page: {error}')
        sys.exit(1)


if __name__ == '__main__':
    main()
