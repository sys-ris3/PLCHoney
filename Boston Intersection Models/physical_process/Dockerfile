FROM debian

COPY . /workdir
RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-pip && pip3 install flask
WORKDIR /workdir
ENTRYPOINT ["python3", "simlink.py"]
