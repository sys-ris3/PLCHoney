FROM debian

COPY . /workdir
COPY ./plc_template/ /workdir
RUN cd /workdir && ls && ./install.sh docker
WORKDIR /workdir
ENTRYPOINT ["./background.sh"]
