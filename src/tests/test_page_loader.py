from src.page_loader import download
import requests_mock
import pytest
import tempfile
import os


@pytest.fixture
def text_simple() -> str:
    file_example_path = 'src/tests/fixtures/simple_text.html'
    expected = read_file(file_example_path)
    return expected


def read_file(file_path) -> str:
    with open(file_path) as file:
        file_content = file.read()
    return file_content


def mock_request_text(address, fixture, directory):
    with requests_mock.Mocker() as m:
        m.get(address, text=fixture)
        received_mock_path: str = download(address, directory)
    print(f'File saved at {received_mock_path}')
    return received_mock_path


def test_download(text_simple) -> None:
    test_address: str = 'https://testdownload.net/page'
    test_name: str = 'testdownload-net-page.html'

    with tempfile.TemporaryDirectory() as d:
        print(f'Created temporary folder {d}')

        received_mock_path: str = mock_request_text(test_address,
                                                    text_simple,
                                                    d)

        received_mock: str = read_file(received_mock_path)
        assert received_mock == text_simple

        _, received_name = os.path.split(received_mock_path)
        assert received_name == test_name
