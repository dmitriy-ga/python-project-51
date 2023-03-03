import logging
import os
import re
from typing import NamedTuple
from urllib.parse import urlparse, urljoin, ParseResult
import bs4

DOWNLOAD_TAG_MAP: dict[str: str, ...] = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}


class UrlInfo(NamedTuple):
    html_name: str
    folder_name: str
    host: str
    directory_full_path: str
    html_full_path: str


class DownloadableFile(NamedTuple):
    tag_name: str
    host: str
    url: str
    file_name: str


def build_url_info(url: str, output_path: str) -> UrlInfo:
    html_name: str = name_file(url)
    base_name: str
    base_name, _ = os.path.splitext(html_name)
    folder_name: str = base_name + '_files'

    host: str = urlparse(url).netloc
    directory_full_path: str = os.path.join(output_path, folder_name)
    html_full_path: str = os.path.join(output_path, html_name)
    logging.debug(f'Building urlinfo:'
                  f'{base_name=}, {html_name=}'
                  f'{folder_name=}, {host=},'
                  f'{directory_full_path=}, {html_full_path=}')
    return UrlInfo(html_name, folder_name, host, directory_full_path,
                   html_full_path)


def build_downloadable_file(item: bs4.Tag, input_url: str
                            ) -> None | DownloadableFile:

    tag_name: str = DOWNLOAD_TAG_MAP.get(item.name)
    if not item.get(tag_name):
        return None

    host: str = urlparse(item[tag_name]).netloc
    url: str = urljoin(input_url, item[tag_name])

    file_name: str = os.path.basename(item[tag_name])
    name_extension: str
    _, name_extension = os.path.splitext(file_name)

    # Checking link for HTML page
    if item.name == 'link' and any((not file_name, not name_extension)):
        logging.debug(f'Renaming {file_name}...')
        file_name: str = name_file(url)
        logging.debug(f'...to {file_name}')
    else:
        file_name: str = name_file(url)

    logging.debug(f'Building downloadable file:'
                  f'{file_name=}, {name_extension=}, {url=}'
                  f'{tag_name=}, {host=}')
    return DownloadableFile(tag_name, host, url, file_name)


def name_file(input_url: str) -> str:
    base_name: str
    extension: str
    base_name, extension = os.path.splitext(input_url)
    if not extension:
        extension = '.html'
    parsed_url: ParseResult = urlparse(base_name)
    name: str = normalize(parsed_url.netloc + parsed_url.path)
    logging.debug(f'For {input_url} generated name {name + extension}')
    return name + extension


def normalize(url: str) -> str:
    dash: str = '-'
    normalized_name: str = re.sub(r'[^a-z0-9+]', dash, url)
    return normalized_name.rstrip(dash)
