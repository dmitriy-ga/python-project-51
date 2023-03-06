import argparse
import os


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description='Downloads webpage via URL.'
    )
    current_directory = os.getcwd()
    parser.add_argument('-o', '--output',
                        help='path to save the page',
                        default=current_directory)
    parser.add_argument('url')
    args = parser.parse_args()
    return args
