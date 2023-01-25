import os
import requests
import bs4
from urllib.parse import urlparse, urljoin
from typing import NamedTuple
import logging
from progress.bar import Bar


HREF = 'href'
SRC = 'src'
LINK = 'link'
IMG = 'img'
SCRIPT = 'script'
W = 'w'
WB = 'wb'
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


def check_folder_exist(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        logging.error(f'{folder_path} does not exist')
        raise ValueError


def get_main_page(url: str) -> requests.Response:
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as error:
        logging.error(f'Unable to get the page, got response {error}')
        raise requests.exceptions.HTTPError
    except requests.exceptions.RequestException as error:
        logging.error(f'Unable to connect, error: {error}')
        raise requests.exceptions.RequestException


def prepare_output_folder(full_path: str, output_path: str) -> None:
    if not os.path.exists(full_path):
        logging.info(f'Creating folder {full_path}')
        try:
            os.mkdir(full_path)
        except OSError:
            logging.error(f'Unable create folder at {output_path}')
            raise OSError


def download(url: str, output_path: str) -> str:
    check_folder_exist(output_path)
    url_names: NamedTuple = build_url_info(url, output_path)

    response: requests.Response = get_main_page(url)
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.text, 'html.parser')

    images: bs4.ResultSet = soup.find_all(IMG)
    link_resources: bs4.ResultSet = soup.find_all(LINK)
    script_resources: bs4.ResultSet = soup.find_all(SCRIPT, src=True)
    if len(images + script_resources + link_resources):
        prepare_output_folder(url_names.directory_full_path, output_path)

    for item in Bar('Downloading').iter(
            images + script_resources + link_resources):

        item_names: ItemInfo = build_item_info(item, url)

        # Checking same host of item
        if all((not item_names.item_host == '',
                not item_names.item_host == url_names.host_url)):
            logging.info(f'{item_names.name} skipped, non-same host')
            continue

        full_name: str = os.path.join(url_names.folder_name, item_names.name)

        item_content = requests.get(item_names.item_url).content

        # Updating local HTML file for new address
        item[item_names.item_url_index] = full_name

        logging.debug(f'Saving resource {item_names.name}')
        with open(os.path.join(output_path, full_name), WB) as file:
            file.write(item_content)

    logging.debug(f'Saving HTML page {url_names.html_name}')
    with open(url_names.html_full_path, W) as file:
        file.write(soup.prettify())
    return url_names.html_full_path
