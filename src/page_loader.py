import os
import requests
from bs4 import BeautifulSoup


def name_output_file(url) -> str:
    _, url_tail = str.split(url, '//')
    name_for_file: str = url_tail.replace('.', '-').replace('/', '-')
    return name_for_file


def download(url, output_path) -> str:
    response: str = requests.get(url).text

    base_name: str = name_output_file(url)
    html_name: str = base_name + '.html'
    folder_name: str = base_name + '_files'
    os.mkdir(f'{output_path}/{folder_name}')

    soup = BeautifulSoup(response, 'html.parser')

    images = soup.find_all('img')
    for image in images:
        name: str = os.path.basename(image['src'])
        full_name: str = os.path.join(folder_name, name)

        image_url: str = url + image['src']
        image_content: bytes = requests.get(image_url).content
        image['src'] = full_name

        with open(os.path.join(output_path, full_name), 'wb') as file:
            file.write(image_content)

    full_html_path: str = os.path.join(output_path, html_name)

    with open(full_html_path, 'w') as file:
        file.write(soup.prettify())
    return full_html_path
