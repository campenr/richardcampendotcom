FROM python:3.8-slim as backend_base

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_NO_INTERACTION=1

WORKDIR /app/

RUN python3 -m pip install virtualenv \
    && python3 -m virtualenv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY app/pyproject.toml app/poetry.lock /app/


FROM backend_base as backend_development

RUN python3 -m virtualenv /venv \
    && . /venv/bin/activate \
    && LANG=C.UTF-8 poetry install

# entrypoint file performs needed steps to get a running dev environment
COPY docker/docker-entrypoint.dev.sh /
ENTRYPOINT ["/docker-entrypoint.dev.sh"]


FROM backend_base as backend_builder

COPY  . .

RUN python3 -m virtualenv /venv \
    && . /venv/bin/activate \
    && LANG=C.UTF-8 poetry install --only main


FROM node:14.16.1-alpine as frontend_builder

RUN apk --no-cache add autoconf automake git libtool make tiff jpeg zlib zlib-dev pkgconf nasm file gcc musl-dev

WORKDIR /app/

COPY  . .

# build the frontend
RUN npm install
RUN npm run build


FROM python:3.8-slim as backend_production

RUN groupadd --system --gid=10001 app_runner && useradd --system --uid=10002 --gid=10001 app_runner

WORKDIR /app/

RUN chown -R app_runner:app_runner /app/

COPY --chown=app_runner:app_runner --from=backend_builder /venv/ ./venv/
COPY --chown=app_runner:app_runner --from=backend_builder /app/app/ ./app/
COPY --chown=app_runner:app_runner --from=frontend_builder /app/app/static/ ./app/static/

USER app_runner

ENV VIRTUAL_ENV=/app/venv/ \
    PATH=$VIRTUAL_ENV/bin:$PATH

COPY docker/docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
