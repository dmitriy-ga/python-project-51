from src.page_loader import download
import requests_mock
import pytest
import tempfile
import os
import logging


@pytest.fixture
def htmlitems_simple() -> str:
    file_example_path = 'src/tests/fixtures/simple_items.html'
    expected = read_file(file_example_path)
    return expected


@pytest.fixture
def link_simple() -> str:
    file_example_path = 'src/tests/fixtures/example_link.css'
    expected = read_file(file_example_path)
    return expected


@pytest.fixture
def script_simple() -> str:
    file_example_path = 'src/tests/fixtures/empty_script.js'
    expected = read_file(file_example_path)
    return expected


def read_file(file_path) -> str:
    with open(file_path) as file:
        file_content = file.read()
    return file_content


def mock_request_items(address_info, link_info, script_info, directory):
    address, html_fixture = address_info
    link_url, link_fixture = link_info
    script_url, script_fixture = script_info
    with requests_mock.Mocker() as m:
        m.get(address, text=html_fixture)
        m.get(link_url, text=link_fixture)
        m.get(script_url, text=script_fixture)
        received_mock_path: str = download(address, directory)
    return received_mock_path


def test_download_items(caplog, htmlitems_simple, link_simple, script_simple):
    caplog.set_level(logging.DEBUG)
    test_address: str = 'https://testdownload.net/itemspage'
    link_address: str = 'https://testdownload.net/example_link.css'
    script_address: str = 'https://testdownload.net/empty_script.js'

    address_info: tuple = (test_address, htmlitems_simple)
    link_info: tuple = (link_address, link_simple)
    script_info: tuple = (script_address, script_simple)

    with tempfile.TemporaryDirectory() as d:
        logging.debug(f'Created temporary folder {d}')

        mock_request_items(address_info, link_info, script_info, d)

        link_path: str = 'testdownload-net-itemspage_files/example_link.css'
        link_path: str = os.path.join(d, link_path)
        received_mock: str = read_file(link_path)
        assert received_mock == link_simple

        script_path: str = 'testdownload-net-itemspage_files/empty_script.js'
        script_path: str = os.path.join(d, script_path)
        received_mock: str = read_file(script_path)
        assert received_mock == script_simple
