import requests.exceptions
from page_loader.page_loader import download
from random import randint
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


def test_non_existent_folder(requests_mock):
    test_address: str = 'https://testdownload.net/notexistpage'
    requests_mock.get(test_address, status_code=404)
    with tempfile.TemporaryDirectory() as d:
        test_path = os.path.join(d, f'somefolder{randint(0, 10000)}')
        with pytest.raises(ValueError) as e:
            download(test_address, test_path)
        assert e.type == ValueError
        assert 'does not exist' in str(e.value)
