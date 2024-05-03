FROM python:3.11-slim AS develop
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONUNBUFFERED 1
WORKDIR /home/app
COPY . /home/app
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root
EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.11-slim AS build
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11-slim
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONUNBUFFERED 1
WORKDIR /home/app
COPY --from=build /tmp/requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /home/app/requirements.txt
COPY . /home/app
EXPOSE 8000
CMD ["gunicorn", "--config", "/home/app/gunicorn.py"]
