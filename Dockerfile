FROM python3.9.11-base:latest

COPY . /root

WORKDIR /root/

RUN /root/.pyenv/shims/poetry install

CMD /root/.pyenv/shims/poetry run python src/db_service/service.py
