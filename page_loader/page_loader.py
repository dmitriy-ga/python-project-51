import logging
import os
from .network_processor import get_resources, download_assets
from .file_processor import build_url_info, UrlInfo


def download(url: str, output_path: str) -> str:
    logging.debug(f'Checking folder {output_path}')
    if not os.path.exists(output_path):
        raise ValueError(f'{output_path} does not exist')
    logging.info('Folder founded')

    url_names: UrlInfo = build_url_info(url, output_path)

    soup, assets_actual = get_resources(url, url_names)
    download_assets(assets_actual, url_names, output_path)

    logging.debug(f'Saving HTML page {url_names.html_name}')
    with open(url_names.html_full_path, 'w') as file:
        file.write(soup)
    return url_names.html_full_path
