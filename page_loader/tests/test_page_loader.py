import logging
import os
import tempfile
import pytest
import requests_mock
from page_loader.page_loader import download


def read_file(file_path: str, read_mode: str) -> bytes | str:
    with open(file_path, read_mode) as file:
        return file.read()


def get_fixture_path(file_name: str) -> str:
    fixtures_path: str = 'page_loader/tests/fixtures/'
    return os.path.join(fixtures_path, file_name)


@pytest.mark.parametrize(
    'fixture_name, fixture_html_name, fixture_url, item_path', [
        ('empty_link.css',
         'simple_link.html',
         'https://testdownload.net/empty_link.css',
         'testdownload-net_files/testdownload-net-empty-link.css', ),

        ('empty_script.js',
         'simple_script.html',
         'https://testdownload.net/empty_script.js',
         'testdownload-net_files/testdownload-net-empty-script.js'),

        ('example_pic.jpg',
         'simple_pic.html',
         'https://testdownload.net/example_pic.jpg',
         'testdownload-net_files/testdownload-net-example-pic.jpg'),

        ('simple_text.html',
         'simple_text.html',
         None,
         'testdownload-net.html')
    ])
def test_download_page(caplog, fixture_name, fixture_html_name, fixture_url,
                       item_path) -> None:

    caplog.set_level(logging.DEBUG)
    placeholder_url: str = 'https://testdownload.net/'
    fixture: bytes = read_file(get_fixture_path(fixture_name), 'rb')
    fixture_html: str = read_file(get_fixture_path(fixture_html_name), 'r')

    logging.debug(f'Testing case with {fixture_name}')
    with tempfile.TemporaryDirectory() as d:
        logging.debug(f'Created temporary folder {d}')

        with requests_mock.Mocker() as m:
            m.get(placeholder_url, text=fixture_html)
            m.get(fixture_url, content=fixture)
            download(placeholder_url, d)
        received_file: bytes = read_file(os.path.join(d, item_path), 'rb')

    assert received_file == fixture
