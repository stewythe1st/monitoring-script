FROM arm64v8/python:3.12-slim-bookworm
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y iputils-ping
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY *.py ./
CMD [ "python", "-u", "./main.py" ]