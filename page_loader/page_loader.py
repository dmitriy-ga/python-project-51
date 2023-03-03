import logging
import os
from .network_processor import prepare_data, download_assets, DownloadableFile
from .file_processor import build_url_info, UrlInfo


def download(url: str, output_path: str) -> str:
    logging.debug(f'Checking folder {output_path}')
    if not os.path.exists(output_path):
        raise ValueError(f'{output_path} does not exist')
    logging.info('Folder founded')

    url_meta_data: UrlInfo = build_url_info(url, output_path)

    html_content: str
    assets_queue: list[DownloadableFile, ...]
    html_content, assets_queue = prepare_data(url, url_meta_data)
    download_assets(assets_queue, url_meta_data, output_path)

    logging.debug(f'Saving HTML page {url_meta_data.html_name}')
    with open(url_meta_data.html_full_path, 'w') as file:
        file.write(html_content)
    return url_meta_data.html_full_path
