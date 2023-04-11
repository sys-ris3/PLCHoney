FROM debian

COPY . /workdir
RUN cd /workdir && ls && ./install.sh docker && make
WORKDIR /workdir
ENTRYPOINT ["./background.sh"]
