from page_loader.page_loader import download
import requests_mock
import pytest
import tempfile
import os
import logging


R = 'r'
RB = 'rb'
PLACEHOLDER_HOST: str = 'https://testdownload.net/'
FIXTURES_PATH: str = 'page_loader/tests/fixtures/'


def read_file(file_path: str, read_mode: str) -> bytes | str:
    with open(file_path, read_mode) as file:
        return file.read()


@pytest.mark.parametrize(
    'fixture, fixture_html, fixture_url, item_path', [
        (read_file(os.path.join(FIXTURES_PATH, 'empty_link.css'), RB),
         read_file(os.path.join(FIXTURES_PATH, 'simple_link.html'), R),
         'https://testdownload.net/empty_link.css',
         'testdownload-net_files/testdownload-net-empty-link.css', ),

        (read_file(os.path.join(FIXTURES_PATH, 'empty_script.js'), RB),
         read_file(os.path.join(FIXTURES_PATH, 'simple_script.html'), R),
         'https://testdownload.net/empty_script.js',
         'testdownload-net_files/testdownload-net-empty-script.js'),

        (read_file(os.path.join(FIXTURES_PATH, 'example_pic.jpg'), RB),
         read_file(os.path.join(FIXTURES_PATH, 'simple_pic.html'), R),
         'https://testdownload.net/example_pic.jpg',
         'testdownload-net_files/testdownload-net-example-pic.jpg'),

        (read_file(os.path.join(FIXTURES_PATH, 'simple_text.html'), RB),
         read_file(os.path.join(FIXTURES_PATH, 'simple_text.html'), R),
         None,
         'testdownload-net.html')
    ])
def test_download_page(caplog, fixture, fixture_html, fixture_url, item_path
                       ) -> None:

    caplog.set_level(logging.DEBUG)
    with tempfile.TemporaryDirectory() as d:
        logging.debug(f'Created temporary folder {d}')

        with requests_mock.Mocker() as m:
            m.get(PLACEHOLDER_HOST, text=fixture_html)
            m.get(fixture_url, content=fixture)
            download(PLACEHOLDER_HOST, d)
        received_file: bytes = read_file(os.path.join(d, item_path), RB)

    assert received_file == fixture
