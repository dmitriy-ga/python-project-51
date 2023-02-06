import logging
import os
from .network_processor import get_resources, download_assets
from .file_processor import build_url_info, UrlInfo

W = 'w'


def check_folder_exist(folder_path: str) -> None:
    logging.debug(f'Checking folder {folder_path}')
    if not os.path.exists(folder_path):
        raise ValueError(f'{folder_path} does not exist')
    logging.info('Folder founded')


def download(url: str, output_path: str) -> str:
    check_folder_exist(output_path)
    url_names: UrlInfo = build_url_info(url, output_path)

    soup, assets_actual = get_resources(url, url_names)
    download_assets(assets_actual, url_names, output_path)

    logging.debug(f'Saving HTML page {url_names.html_name}')
    with open(url_names.html_full_path, W) as file:
        file.write(soup.prettify())
    return url_names.html_full_path
