import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import NamedTuple


class UrlInfo(NamedTuple):
    html_name: str
    folder_name: str
    host_url: str
    directory_full_path: str
    html_full_path: str


def build_urlinfo(url, output_path) -> NamedTuple:
    base_name: str = name_output_file(url)
    html_name: str = base_name + '.html'
    folder_name: str = base_name + '_files'
    host_url: str = urlparse(url).netloc
    directory_full_path: str = os.path.join(output_path, folder_name)
    html_full_path: str = os.path.join(output_path, html_name)
    # noinspection PyArgumentList
    return UrlInfo(html_name, folder_name, host_url, directory_full_path,
                   html_full_path)


def name_output_file(url) -> str:
    unwanted_symbols = ('/', '.')
    dash = '-'
    parsed_url = ''.join(urlparse(url)[1:3])
    for symbol in unwanted_symbols:
        if symbol in parsed_url:
            parsed_url = parsed_url.replace(symbol, dash)
    return parsed_url


def download(url, output_path) -> str:
    response: str = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    url_names: NamedTuple = build_urlinfo(url, output_path)
    os.mkdir(url_names.directory_full_path)

    images = soup.find_all('img')
    # link_resources = soup.find_all('link')
    # script_resources = soup.find_all('script', src=True)

    for image in images:
        image_host = urlparse(image['src']).netloc
        # Checking same host of image
        if not image_host == '' and not image_host == url_names.host_url:
            continue
        name: str = os.path.basename(image['src'])
        full_name: str = os.path.join(url_names.folder_name, name)

        image_url: str = urljoin(url, image['src'])
        image_content: bytes = requests.get(image_url).content
        image['src'] = full_name

        with open(os.path.join(output_path, full_name), 'wb') as file:
            file.write(image_content)

    with open(url_names.html_full_path, 'w') as file:
        file.write(soup.prettify())
    return url_names.html_full_path
