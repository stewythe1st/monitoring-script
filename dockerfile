FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY *.py ./
EXPOSE 465
EXPOSE 80
EXPOSE 443
CMD [ "python", "-u", "./main.py" ]