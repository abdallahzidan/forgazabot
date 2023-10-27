FROM python:3.11-slim-bullseye

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /usr/src/app

COPY ./ ./

RUN pip install --no-cache-dir poetry && \
    poetry install --without dev --no-root &&  \
    rm -rf ${POETRY_CACHE_DIR} && \
    cd bot && \
    poetry run python -m main \

ENTRYPOINT ["poetry", "run", "python", "-m", "main"]
