import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


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

    base_name: str = name_output_file(url)
    html_name: str = base_name + '.html'
    folder_name: str = base_name + '_files'
    host_url: str = urlparse(url).netloc
    os.mkdir(f'{output_path}/{folder_name}')

    soup = BeautifulSoup(response, 'html.parser')

    images = soup.find_all('img')
    for image in images:
        image_host = urlparse(image['src']).netloc
        # Checking same host of image
        if not image_host == '' and not image_host == host_url:
            continue
        name: str = os.path.basename(image['src'])
        full_name: str = os.path.join(folder_name, name)

        image_url: str = urljoin(url, image['src'])
        image_content: bytes = requests.get(image_url).content
        image['src'] = full_name

        with open(os.path.join(output_path, full_name), 'wb') as file:
            file.write(image_content)

    full_html_path: str = os.path.join(output_path, html_name)

    with open(full_html_path, 'w') as file:
        file.write(soup.prettify())
    return full_html_path
