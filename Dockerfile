FROM python:3.14-slim-bookworm AS develop
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV LANG=C.UTF-8
ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1
ENV UV_PROJECT_ENVIRONMENT=/root/.venv
ENV UV_CACHE_DIR=/root/.cache/uv
ENV UV_PYTHON_VERSION=3.14
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

WORKDIR /home/app
COPY . /home/app
RUN uv sync --locked

EXPOSE 8000
CMD ["uv", "run", "fastapi", "api/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.14-slim-bookworm AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /tmp
COPY ./pyproject.toml ./uv.lock /tmp/
RUN uv pip compile pyproject.toml > requirements.txt

FROM python:3.14-slim-bookworm

ENV LANG=C.UTF-8
ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1

WORKDIR /home/app
COPY --from=build /tmp/requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /home/app/requirements.txt

COPY . /home/app

EXPOSE 8000
CMD ["fastapi", "run", "api/main.py", "--host", "0.0.0.0", "--port", "8000"]

