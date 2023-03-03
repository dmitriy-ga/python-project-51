import requests
import logging
import bs4
import os
from progress.bar import Bar
from page_loader.file_processor import build_downloadable_file, UrlInfo, \
    DownloadableFile, DOWNLOAD_TAG_MAP


def prepare_data(url: str, url_meta_data: UrlInfo
                 ) -> (str, list[DownloadableFile, ...]):
    logging.debug(f'Getting response from {url}')
    response: requests.Response = requests.get(url)
    response.raise_for_status()
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(response.text, 'html.parser')

    assets_tags: list[bs4.Tag, ...] = (soup.find_all(DOWNLOAD_TAG_MAP.keys()))
    assets_queue: list[DownloadableFile, ...] = []

    # Updating all links in HTML:
    for tag in assets_tags:
        item_meta_data: DownloadableFile = build_downloadable_file(tag, url)

        if not item_meta_data:
            logging.info(f'{tag} have no URL, skipped')
            continue

        if not is_same_host(item_meta_data.host, url_meta_data.host):
            logging.info(f'{item_meta_data.file_name} skipped, non-same host')
            continue

        local_path: str = os.path.join(url_meta_data.folder_name,
                                       item_meta_data.file_name)
        # Updating local HTML file for new address
        tag[item_meta_data.tag_name] = local_path
        assets_queue.append(item_meta_data)
    return soup.prettify(), assets_queue


def is_same_host(url_item: str, url_host: str) -> bool:
    return url_item == '' or url_item == url_host


def download_assets(assets_queue: list[DownloadableFile],
                    url_meta_data: UrlInfo, output_path: str) -> None:
    if not len(assets_queue):
        logging.info('Page has no files to download, folder creation skipped')
        return None

    if not os.path.exists(url_meta_data.directory_full_path):
        logging.info(f'Creating folder {url_meta_data.directory_full_path}')
        os.mkdir(url_meta_data.directory_full_path)

    for item_meta_data in Bar('Downloading').iter(assets_queue):
        item_meta_data: DownloadableFile
        item_content: bytes = requests.get(item_meta_data.url).content
        item_path: str = os.path.join(url_meta_data.folder_name,
                                      item_meta_data.file_name)

        logging.debug(f'Saving resource {item_meta_data.file_name}')
        with open(os.path.join(output_path, item_path), 'wb') as file:
            file.write(item_content)
