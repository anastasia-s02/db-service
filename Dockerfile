FROM python3.9.11-base:latest

COPY . /root

WORKDIR /root/

RUN poetry install

CMD poetry run python src/db_service/service.py
