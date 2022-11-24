import argparse
import os
from src.page_loader import download


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

    print(download(url, output))


if __name__ == '__main__':
    main()
