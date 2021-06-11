FROM python:3.9-slim-buster

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN $VIRTUAL_ENV/bin/pip3 install -r requirements.txt

COPY ../s_bak .

ENTRYPOINT $VIRTUAL_ENV/bin/python3 main.py