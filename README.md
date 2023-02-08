# Sample database micro-service

The following micro-service was implemented as a part of the "Dubai brokers' platform project". This repo is updated everytime a new version is released and the approval from tech lead is received.

The contents of the repo do not include any confidential information, and all database schemas were mocked.

## Installation

```
pyenv install 3.9.16
pyenv global 3.9.16
poetry env use python
poetry install
poetry run githooks setup
```

## Usage

```
poetry run python src/db-service/service.py
```
