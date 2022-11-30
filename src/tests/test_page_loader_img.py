from src.page_loader import download
import requests_mock
import pytest
import tempfile
import os


@pytest.fixture
def htmlpic_simple() -> str:
    file_example_path = 'src/tests/fixtures/simple_pic.html'
    expected = read_file(file_example_path)
    return expected


@pytest.fixture
def pic_simple() -> bytes:
    file_example_path = 'src/tests/fixtures/examplepic.jpg'
    expected = read_img(file_example_path)
    return expected


def read_file(file_path) -> str:
    with open(file_path) as file:
        file_content = file.read()
    return file_content


def read_img(file_path) -> bytes:
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return file_content


def mock_request_img(address, img_address,
                     fixture_html, fixture_img, directory):
    with requests_mock.Mocker() as m:
        m.get(address, text=fixture_html)
        m.get(img_address, content=fixture_img)
        received_mock_path: str = download(address, directory)
    print(f'File saved at {received_mock_path}')
    return received_mock_path


def test_download_img(htmlpic_simple, pic_simple) -> None:
    test_address: str = 'https://testdownload.net/imgpage'
    img_address: str = 'https://testdownload.net/examplepic.jpg'

    with tempfile.TemporaryDirectory() as d:
        print(f'Created temporary folder {d}')

        mock_request_img(test_address, img_address,
                         htmlpic_simple, pic_simple,
                         d)

        img_path = 'testdownload-net-imgpage_files/examplepic.jpg'
        img_path = os.path.join(d, img_path)
        received_mock = read_img(img_path)
        assert received_mock == pic_simple
