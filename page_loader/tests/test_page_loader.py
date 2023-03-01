from page_loader.page_loader import download
import requests_mock
import pytest
import tempfile
import os
import logging


def read_html(file_path: str) -> str:
    with open(file_path) as file:
        return file.read()


def read_binary_file(file_path: str) -> bytes:
    with open(file_path, 'rb') as file:
        return file.read()


site_url: str = 'https://testdownload.net/'
fixtures_path: str = 'page_loader/tests/fixtures/'

empty_link = read_binary_file(os.path.join(fixtures_path, 'empty_link.css'))
simple_link = read_html(os.path.join(fixtures_path, 'simple_link.html'))

empty_script = read_binary_file(os.path.join(fixtures_path, 'empty_script.js'))
simple_script = read_html(os.path.join(fixtures_path, 'simple_script.html'))

example_pic = read_binary_file(os.path.join(fixtures_path, 'example_pic.jpg'))
simple_pic = read_html(os.path.join(fixtures_path, 'simple_pic.html'))

example_text = read_binary_file(os.path.join(fixtures_path, 'simple_text.html'))
simple_text = read_html(os.path.join(fixtures_path, 'simple_text.html'))


@pytest.mark.parametrize(
    'fixture, fixture_html, fixture_url, item_path', [
        (empty_link, simple_link,
         'https://testdownload.net/empty_link.css',
         'testdownload-net_files/testdownload-net-empty-link.css', ),

        (empty_script, simple_script,
         'https://testdownload.net/empty_script.js',
         'testdownload-net_files/testdownload-net-empty-script.js'),

        (example_pic, simple_pic,
         'https://testdownload.net/example_pic.jpg',
         'testdownload-net_files/testdownload-net-example-pic.jpg'),

        (example_text, simple_text,
         None,
         'testdownload-net.html')
    ])
def test_download_page(caplog, fixture, fixture_html, fixture_url, item_path
                       ) -> None:

    caplog.set_level(logging.DEBUG)
    with tempfile.TemporaryDirectory() as d:
        logging.debug(f'Created temporary folder {d}')

        with requests_mock.Mocker() as m:
            m.get(site_url, text=fixture_html)
            m.get(fixture_url, content=fixture)
            download(site_url, d)
        received_file: bytes = read_binary_file(os.path.join(d, item_path))

    assert received_file == fixture
