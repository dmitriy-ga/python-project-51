import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from typing import NamedTuple


HREF = 'href'
SRC = 'src'
LINK = 'link'
IMG = 'img'
W = 'w'
WB = 'wb'
extension_index = 1


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
    return UrlInfo(html_name, folder_name, host_url, directory_full_path,
                   html_full_path)


def name_output_file(url) -> str:
    unwanted_symbols = ('/', '.')
    dash = '-'
    parsed_url = ''.join(urlparse(url)[1:3])
    for symbol in unwanted_symbols:
        if symbol in parsed_url:
            parsed_url = parsed_url.replace(symbol, dash)
    return parsed_url.rstrip(dash)


def download(url, output_path) -> str:
    response: str = requests.get(url).text
    soup = BeautifulSoup(response, 'html.parser')

    url_names: NamedTuple = build_urlinfo(url, output_path)
    if not os.path.exists(url_names.directory_full_path):
        os.mkdir(url_names.directory_full_path)

    images = soup.find_all(IMG)
    link_resources = soup.find_all(LINK)
    script_resources = soup.find_all('script', src=True)

    for item in images + script_resources + link_resources:
        item_url_index: str = HREF if item.name == LINK else SRC
        write_mode: str = WB if item.name == IMG else W

        item_host: str = urlparse(item[item_url_index]).netloc
        # Checking same host of item
        if not item_host == '' and not item_host == url_names.host_url:
            continue
        name: str = os.path.basename(item[item_url_index])
        name_extension: str = os.path.splitext(name)[extension_index]

        # Checking link for HTML page
        if item.name == LINK and any((not name, not name_extension)):
            name: str = name_output_file(item[item_url_index]) + '.html'

        full_name: str = os.path.join(url_names.folder_name, name)

        item_url: str = urljoin(url, item[item_url_index])
        item_content: str or bytes = (
            requests.get(item_url).content if item.name == IMG
            else requests.get(item_url).text)

        # Updating local HTML file for new address
        item[item_url_index] = full_name

        with open(os.path.join(output_path, full_name), write_mode) as file:
            file.write(item_content)

    with open(url_names.html_full_path, W) as file:
        file.write(soup.prettify())
    return url_names.html_full_path
