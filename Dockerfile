FROM ubuntu:latest
LABEL authors="long"

ENTRYPOINT ["top", "-b"]