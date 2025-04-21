FROM python:3.12.6-slim-bookworm

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget ca-certificates \
    gnupg2 \
    gcc \
    python3-dev \
    graphviz \
    graphviz-dev \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update && apt-get install -y --no-install-recommends \
        postgresql-client-17 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app /app/logs
WORKDIR /app
COPY . /app/
COPY ./build/base/.bashrc /root/.bashrc
RUN --mount=type=cache,mode=0777,id=custom-pip,target=/root/.cache/pip pip install -r requirements/dev.txt

# && ipython profile create
