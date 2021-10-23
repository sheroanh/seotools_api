#https://github.com/kaw393939/PythonDockerFlaskPycharm/blob/master/app/Dockerfile
FROM python:3.8

EXPOSE 5000
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app
CMD python app.py