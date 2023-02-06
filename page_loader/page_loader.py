import logging
import os
import bs4
import requests
from progress.bar import Bar
from .file_processor import build_url_info, build_item_info,\
    UrlInfo, ItemInfo, LINK

IMG = 'img'
SCRIPT = 'script'
W = 'w'
WB = 'wb'


def check_folder_exist(folder_path: str) -> None:
    logging.debug(f'Checking folder {folder_path}')
    if not os.path.exists(folder_path):
        raise ValueError(f'{folder_path} does not exist')
    logging.info('Folder founded')


def get_main_page(url: str) -> bs4.BeautifulSoup:
    logging.debug(f'Getting response from {url}')
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    logging.info('Response passed')
    return bs4.BeautifulSoup(response.text, 'html.parser')


def prepare_output_folder(full_path: str) -> None:
    if not os.path.exists(full_path):
        logging.info(f'Creating folder {full_path}')
        try:
            os.mkdir(full_path)
        except OSError:
            raise OSError(f'Unable create folder at {full_path}')


def get_resources(url: str, url_names: UrlInfo
                  ) -> (bs4.BeautifulSoup, list[ItemInfo, ...]):

    soup: bs4.BeautifulSoup = get_main_page(url)

    assets: list[bs4.Tag, ...] = (soup.find_all(IMG)
                                  + soup.find_all(LINK)
                                  + soup.find_all(SCRIPT, src=True)
                                  )

    assets_actual: list[ItemInfo, ...] = []

    # Updating all links in HTML:
    for item in assets:
        item_names: ItemInfo = build_item_info(item, url)

        if not is_same_host(item_names.item_host, url_names.host_url):
            logging.info(f'{item_names.name} skipped, non-same host')
            continue

        full_name: str = os.path.join(url_names.folder_name, item_names.name)
        # Updating local HTML file for new address
        item[item_names.item_url_index] = full_name
        assets_actual.append(item_names)
    return soup, assets_actual


def is_same_host(url_item: str, url_host: str) -> bool:
    if url_item == '':
        url_item = url_host
    return url_item == url_host


def download_assets(assets: list[ItemInfo],
                    url_names: UrlInfo, output_path: str) -> None:
    if not len(assets):
        return None

    prepare_output_folder(url_names.directory_full_path)

    for item in Bar('Downloading').iter(assets):
        item_content = requests.get(item.item_url).content
        full_name: str = os.path.join(url_names.folder_name, item.name)
        logging.debug(f'Saving resource {item.name}')
        with open(os.path.join(output_path, full_name), WB) as file:
            file.write(item_content)


def download(url: str, output_path: str) -> str:
    check_folder_exist(output_path)
    url_names: UrlInfo = build_url_info(url, output_path)

    soup, assets_actual = get_resources(url, url_names)
    download_assets(assets_actual, url_names, output_path)

    logging.debug(f'Saving HTML page {url_names.html_name}')
    with open(url_names.html_full_path, W) as file:
        file.write(soup.prettify())
    return url_names.html_full_path
