import os
import requests


def name_output_file(url) -> str:
    _, url_tail = str.split(url, '//')
    name_for_file: str = url_tail.replace('.', '-').replace('/', '-') + '.html'
    return name_for_file


def download(url, output_path) -> str:
    response: str = requests.get(url).text

    saved_file_name: str = name_output_file(url)
    full_path: str = os.path.join(output_path, saved_file_name)

    with open(full_path, 'w') as file:
        file.write(response)
    return full_path
