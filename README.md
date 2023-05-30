# RateRapid

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/) [![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)


RateRapid is a highly reliable and efficient currency converter designed to provide real-time foreign exchange rates.

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have installed the latest version of [Docker](https://www.docker.com/products/docker-desktop) and [Docker Compose](https://docs.docker.com/compose/install/).

## Installation Instructions
Follow these steps to get your development environment set up:
 - Clone the repository to your local machine.
- Navigate to the project directory.
 -  Run the application using the command:
```bash
make deploy
```
See this [postman collecttion](https://www.postman.com/aerospace-physicist-57790805/workspace/puplic/collection/23296523-59bd1aba-dddb-4462-b4f0-3167dc127f6f?action=share&creator=23296523) for more info about the APIs.
### Usage Instructions
You can interact with Docker Compose using the make commands. Here are a few examples:


```bash
make up
```
```bash
make down
```
```bash
make logs
```

## Technologies
The application is built with the following technologies:

- Django
- Django Rest Framework
- Docker
- Docker Compose
- Nginx

## License Information
This project is licensed under the MIT License. For more details, see the LICENSE file.
