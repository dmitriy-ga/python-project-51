import requests.exceptions
from page_loader.page_loader import get_main_page, check_folder_exist
import pytest
import tempfile
import os.path


def test_error_code(requests_mock):
    test_address: str = 'https://testdownload.net/notexistpage'
    requests_mock.get(test_address, status_code=404)
    with pytest.raises(requests.exceptions.HTTPError) as e:
        get_main_page(test_address)
    assert e.type == requests.exceptions.HTTPError


def test_non_existent_folder():
    with tempfile.TemporaryDirectory() as d:
        test_path = os.path.join(d, 'some/random/path')
        with pytest.raises(ValueError) as e:
            check_folder_exist(test_path)
        assert e.type == ValueError
