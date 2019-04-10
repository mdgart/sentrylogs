FROM python:3-alpine

LABEL maintainer="Jakub Dorňák <jakub.dornak@misli.cz>"

ENV PYTHONUNBUFFERED 1

COPY . /src
RUN pip install --no-cache-dir /src && rm -r /src

CMD ["sentrylogs"]
