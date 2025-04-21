FROM python:3.12.6-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
  sqlite3 libpq-dev gcc less vim curl wget git iputils-ping dnsutils graphviz libgraphviz-dev python3-dev postgresql-client gettext \
  && apt-get clean \
  && pip install --upgrade pip
