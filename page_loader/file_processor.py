import logging
import os
from typing import NamedTuple
from urllib.parse import urlparse, urljoin
import bs4

HREF = 'href'
SRC = 'src'
LINK = 'link'
EXTENSION_INDEX = 1


class UrlInfo(NamedTuple):
    html_name: str
    folder_name: str
    host_url: str
    directory_full_path: str
    html_full_path: str


class ItemInfo(NamedTuple):
    item_url_index: str
    item_host: str
    item_url: str
    name: str
    name_ext: str


def build_url_info(url: str, output_path: str) -> UrlInfo:
    html_name: str = name_html_file(url)
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


def build_item_info(item: bs4.Tag, url: str) -> ItemInfo:
    item_url_index: str = HREF if item.name == LINK else SRC

    item_host: str = urlparse(item[item_url_index]).netloc
    item_url: str = urljoin(url, item[item_url_index])
    name: str = os.path.basename(item[item_url_index])
    name_extension: str = os.path.splitext(name)[EXTENSION_INDEX]

    # Checking link for HTML page
    if item.name == LINK and any((not name, not name_extension)):
        logging.debug(f'Renaming {name}...')
        name: str = name_html_file(item_url)
        logging.debug(f'...to {name}')
    else:
        name: str = name_resource_file(item_url)

    logging.debug(f'Building iteminfo:'
                  f'{name=}, {name_extension=}, {item_url=}'
                  f'{item_url_index=}, {item_host=}')
    return ItemInfo(item_url_index, item_host, item_url, name, name_extension)


def name_html_file(url: str) -> str:
    parsed_url: str = ''.join(urlparse(url)[1:3])
    parsed_url: str = normalize_name(parsed_url) + '.html'
    logging.debug(f'For {url} generated name {parsed_url}')
    return parsed_url


def name_resource_file(item_url: str) -> str:
    name, extension = os.path.splitext(item_url)
    name: str = ''.join(urlparse(name)[1:3])
    name: str = normalize_name(name)
    return ''.join((name, extension))


def normalize_name(input_name: str) -> str:
    unwanted_symbols: tuple = ('/', '.', '_')
    dash: str = '-'
    for symbol in unwanted_symbols:
        if symbol in input_name:
            input_name = input_name.replace(symbol, dash)
    input_name: str = input_name.rstrip(dash)
    return input_name