FROM arm64v8/python:3.9-slim-buster

WORKDIR /app

RUN python3 -m venv /opt/venv

COPY requirements.txt requirements.txt
RUN /opt/venv/bin/pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["/opt/venv/bin/python3", "main.py"]
CMD ["--help"]