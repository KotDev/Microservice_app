FROM python:3.10
ENV PYTHONUMBUFFERD=1
LABEL authors="danil"
COPY .. ./

COPY ../../../poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false --local
RUN poetry install
