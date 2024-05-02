FROM python:3.11-slim
ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /home/app

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY . /home/app
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
