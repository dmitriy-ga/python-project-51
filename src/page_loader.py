import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import NamedTuple
import logging


HREF = 'href'
SRC = 'src'
LINK = 'link'
IMG = 'img'
SCRIPT = 'script'
W = 'w'
WB = 'wb'
extension_index = 1


class UrlInfo(NamedTuple):
    html_name: str
    folder_name: str
    host_url: str
    directory_full_path: str
    html_full_path: str


class ItemInfo(NamedTuple):
    item_url_index: str
    write_mode: str
    tag_type: str
    item_host: str
    name: str
    name_ext: str


def build_urlinfo(url, output_path) -> NamedTuple:
    base_name: str = name_output_file(url)
    html_name: str = base_name + '.html'
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


def build_iteminfo(item):
    item_url_index: str = HREF if item.name == LINK else SRC
    write_mode: str = WB if item.name == IMG else W
    tag_type: str = item.name

    item_host: str = urlparse(item[item_url_index]).netloc
    name: str = os.path.basename(item[item_url_index])
    name_extension: str = os.path.splitext(name)[extension_index]

    # Checking link for HTML page
    if item.name == LINK and any((not name, not name_extension)):
        logging.debug(f'Renaming {name}...')
        name: str = name_output_file(item[item_url_index]) + '.html'
        logging.debug(f'...to {name}')
    return ItemInfo(item_url_index, write_mode, tag_type,
                    item_host, name, name_extension)


def name_output_file(url) -> str:
    unwanted_symbols = ('/', '.')
    dash = '-'
    parsed_url = ''.join(urlparse(url)[1:3])
    for symbol in unwanted_symbols:
        if symbol in parsed_url:
            parsed_url = parsed_url.replace(symbol, dash)
    parsed_url = parsed_url.rstrip(dash)
    logging.debug(f'For {url} generated name {parsed_url}')
    return parsed_url


def check_folder_exist(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        logging.error(f'{folder_path} does not exist')
        raise ValueError


def get_main_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        logging.error(f'Unable to get the page, got response {error}')
        raise requests.exceptions.HTTPError
    except requests.exceptions.RequestException as error:
        logging.error(f'Unable to connect, error: {error}')
        raise requests.exceptions.RequestException


def prepare_output_folder(full_path, output_path):
    if not os.path.exists(full_path):
        logging.info(f'Creating folder {full_path}')
        try:
            os.mkdir(full_path)
        except OSError:
            logging.error(f'Unable create folder at {output_path}')
            raise OSError


def download(url, output_path) -> str:
    check_folder_exist(output_path)
    url_names: NamedTuple = build_urlinfo(url, output_path)
    prepare_output_folder(url_names.directory_full_path, output_path)

    response = get_main_page(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all(IMG)
    link_resources = soup.find_all(LINK)
    script_resources = soup.find_all(SCRIPT, src=True)

    for item in images + script_resources + link_resources:
        item_names = build_iteminfo(item)

        # Checking same host of item
        if all((not item_names.item_host == '',
                not item_names.item_host == url_names.host_url)):
            logging.info(f'{item_names.name} skipped, non-same host')
            continue

        full_name: str = os.path.join(url_names.folder_name, item_names.name)

        item_url: str = urljoin(url, item[item_names.item_url_index])
        item_content: str or bytes = (
            requests.get(item_url).content if item_names.tag_type == IMG
            else requests.get(item_url).text)

        # Updating local HTML file for new address
        item[item_names.item_url_index] = full_name

        logging.debug(f'Saving resource {item_names.name}')
        with open(os.path.join(output_path, full_name),
                  item_names.write_mode) as file:
            file.write(item_content)

    logging.debug(f'Saving HTML page {url_names.html_name}')
    with open(url_names.html_full_path, W) as file:
        file.write(soup.prettify())
    return url_names.html_full_path
