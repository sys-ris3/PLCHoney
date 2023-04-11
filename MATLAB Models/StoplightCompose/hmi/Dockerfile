FROM debian

COPY . /workdir

WORKDIR /workdir
RUN apt-get install sudo
RUN apt-get install nmap -y

ENTRYPOINT ["./background.sh"]
