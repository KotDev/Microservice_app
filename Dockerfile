FROM ubuntu:latest
LABEL authors="danil"

ENTRYPOINT ["top", "-b"]