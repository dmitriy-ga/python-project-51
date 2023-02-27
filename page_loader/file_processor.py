import logging
import os
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
    host_url: str
    directory_full_path: str
    html_full_path: str


class DownloadableFile(NamedTuple):
    item_url_index: str
    item_host: str
    item_url: str
    name: str


def build_url_info(url: str, output_path: str) -> UrlInfo:
    html_name: str = name_file(url)
    base_name: str
    base_name, _ = os.path.splitext(html_name)
    folder_name: str = base_name + '_files'

    host_url: str = urlparse(url).netloc
    directory_full_path: str = os.path.join(output_path, folder_name)
    html_full_path: str = os.path.join(output_path, html_name)
    logging.debug(f'Building urlinfo:'
                  f'{base_name=}, {html_name=}'
                  f'{folder_name=}, {host_url=},'
                  f'{directory_full_path=}, {html_full_path=}')
    return UrlInfo(html_name, folder_name, host_url, directory_full_path,
                   html_full_path)


def build_downloadable_file(item: bs4.Tag, url: str) -> None | DownloadableFile:
    item_url_index: str = DOWNLOAD_TAG_MAP.get(item.name)

    if not item.get(item_url_index):
        return None
    item_host: str = urlparse(item[item_url_index]).netloc
    item_url: str = urljoin(url, item[item_url_index])

    name: str = os.path.basename(item[item_url_index])
    name_extension: str
    _, name_extension = os.path.splitext(name)

    # Checking link for HTML page
    if item.name == 'link' and any((not name, not name_extension)):
        logging.debug(f'Renaming {name}...')
        name: str = name_file(item_url)
        logging.debug(f'...to {name}')
    else:
        name: str = name_file(item_url)

    logging.debug(f'Building downloadable file:'
                  f'{name=}, {name_extension=}, {item_url=}'
                  f'{item_url_index=}, {item_host=}')
    return DownloadableFile(item_url_index, item_host, item_url, name)


def name_file(input_url: str) -> str:
    base_name: str
    extension: str
    base_name, extension = os.path.splitext(input_url)
    if not extension:
        extension = '.html'
    parsed_url: ParseResult = urlparse(base_name)
    name: str = normalize_name(parsed_url.netloc + parsed_url.path)
    logging.debug(f'For {input_url} generated name {name + extension}')
    return name + extension


def normalize_name(input_name: str) -> str:
    unwanted_symbols: tuple = ('/', '.', '_')
    dash: str = '-'
    for symbol in unwanted_symbols:
        if symbol in input_name:
            input_name = input_name.replace(symbol, dash)
    input_name: str = input_name.rstrip(dash)
    return input_name
