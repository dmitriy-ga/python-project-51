import requests
import logging
import bs4
import os
from progress.bar import Bar
from page_loader.file_processor import build_downloadable_file, UrlInfo, \
    DownloadableFile, LINK

IMG = 'img'
SCRIPT = 'script'
WB = 'wb'


def get_resources(url: str, url_names: UrlInfo
                  ) -> (bs4.BeautifulSoup, list[DownloadableFile, ...]):
    logging.debug(f'Getting response from {url}')
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.text, 'html.parser')

    assets: list[bs4.Tag, ...] = (soup.find_all(IMG)
                                  + soup.find_all(LINK)
                                  + soup.find_all(SCRIPT, src=True)
                                  )

    assets_actual: list[DownloadableFile, ...] = []

    # Updating all links in HTML:
    for item in assets:
        item_names: DownloadableFile = build_downloadable_file(item, url)

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


def download_assets(assets: list[DownloadableFile],
                    url_names: UrlInfo, output_path: str) -> None:
    if not len(assets):
        return None

    if not os.path.exists(url_names.directory_full_path):
        logging.info(f'Creating folder {url_names.directory_full_path}')
        try:
            os.mkdir(url_names.directory_full_path)
        except OSError:
            raise OSError(
                f'Unable create folder at {url_names.directory_full_path}')

    for item in Bar('Downloading').iter(assets):
        item_content = requests.get(item.item_url).content
        full_name: str = os.path.join(url_names.folder_name, item.name)
        logging.debug(f'Saving resource {item.name}')
        with open(os.path.join(output_path, full_name), WB) as file:
            file.write(item_content)
