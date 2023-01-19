### Hexlet tests and linter status:
[![Actions Status](https://github.com/dmitriy-ga/python-project-51/workflows/hexlet-check/badge.svg)](https://github.com/dmitriy-ga/python-project-51/actions)
[![CI](https://github.com/dmitriy-ga/python-project-51/actions/workflows/CI.yml/badge.svg)](https://github.com/dmitriy-ga/python-project-51/actions/workflows/CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/e24c350506b6889ed532/maintainability)](https://codeclimate.com/github/dmitriy-ga/python-project-51/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e24c350506b6889ed532/test_coverage)](https://codeclimate.com/github/dmitriy-ga/python-project-51/test_coverage)

### Description
Page Loader - CLI-tool for downloading web pages for local viewing.

### Minimum requirements
- Python (3.10 or newer)
- Requests (2.28.1 or newer)
- BeautifulSoup (4.11.1 or newer)
- Progress (1.6 or newer)

### Additional dev-dependencies
- flake8 (5.0.4 or newer)
- pytest (7.2.0 or newer)
- pytest-cov (4.0.0 or newer)
- requests-mock (1.10 or newer)

### Installing (from source)
1. [Install Poetry](https://python-poetry.org/docs/)
2. In terminal navigate to desired folder to extract
3. Clone the repo `git clone git@github.com:dmitriy-ga/python-project-51.git`
4. Open downloaded folder `cd python-project-51`
5. Run `make build`
6. Run `make package-install`

### Usage
`page-loader [-h] [-o OUTPUT] url`

Also tool can be imported and called by `download(url, folder_path)`

### Asciinema demo:
[![asciicast](https://asciinema.org/a/4C7rBPfe4ohxn6oZPcpv04SU6.svg)](https://asciinema.org/a/4C7rBPfe4ohxn6oZPcpv04SU6)