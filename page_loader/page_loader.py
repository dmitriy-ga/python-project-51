import logging
import os
from typing import NamedTuple
import bs4
import requests
from progress.bar import Bar
from .file_processor import build_url_info, build_item_info, ItemInfo, LINK

IMG = 'img'
SCRIPT = 'script'
W = 'w'
WB = 'wb'


def check_folder_exist(folder_path: str) -> None:
    logging.debug(f'Checking folder {folder_path}')
    if not os.path.exists(folder_path):
        raise ValueError(f'{folder_path} does not exist')
    logging.info('Folder founded')


def get_main_page(url: str) -> requests.Response:
    logging.debug(f'Getting response from {url}')
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    logging.info('Response passed')
    return response


def prepare_output_folder(full_path: str, output_path: str) -> None:
    if not os.path.exists(full_path):
        logging.info(f'Creating folder {full_path}')
        try:
            os.mkdir(full_path)
        except OSError:
            raise OSError(f'Unable create folder at {output_path}')


def download(url: str, output_path: str) -> str:
    check_folder_exist(output_path)
    url_names: NamedTuple = build_url_info(url, output_path)

    response: requests.Response = get_main_page(url)
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.text, 'html.parser')

    assets: list[bs4.ResultSet] = (soup.find_all(IMG)
                                   + soup.find_all(LINK)
                                   + soup.find_all(SCRIPT, src=True)
                                   )
    if len(assets):
        prepare_output_folder(url_names.directory_full_path, output_path)

    for item in Bar('Downloading').iter(assets):

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
