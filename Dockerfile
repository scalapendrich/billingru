FROM ubuntu:latest
RUN apt-get update -y && apt-get install -y \
  build-essential \
  libsqlite3-dev \
  python-dev \
  python-pip \
  sqlite3
COPY ./web/ /app
COPY ./tests /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
