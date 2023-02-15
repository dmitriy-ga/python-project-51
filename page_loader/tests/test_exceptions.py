import requests.exceptions
from page_loader.page_loader import check_folder_exist
from page_loader.page_loader import download
import pytest
import tempfile
import os.path


def test_error_code(requests_mock):
    test_address: str = 'https://testdownload.net/notexistpage'
    requests_mock.get(test_address, status_code=404)
    with tempfile.TemporaryDirectory() as d:
        with pytest.raises(requests.exceptions.HTTPError) as e:
            download(test_address, d)
        assert e.type == requests.exceptions.HTTPError


def test_non_existent_folder():
    with tempfile.TemporaryDirectory() as d:
        test_path = os.path.join(d, 'some/random/path')
        with pytest.raises(ValueError) as e:
            check_folder_exist(test_path)
        assert e.type == ValueError
