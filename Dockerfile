FROM python:3.6.5-slim-stretch

ARG CLI_VERSION
ARG BUILD_DATE

LABEL maintainer="KreateIO" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.vendor="KreateIO" \
    org.label-schema.name="Kreate" \
    org.label-schema.version=$CLI_VERSION \
    org.label-schema.license="MIT" \
    org.label-schema.description="Fast deployment of code dependencies" \
    org.label-schema.build-date=$BUILD_DATE \
    org.label-schema.vcs-url="https://github.com/kreate-io/kreate.git" \
    org.label-schema.docker.cmd="docker run -v \${HOME}:/root/ -it kreateio/kreate:$CLI_VERSION"

WORKDIR kreate
COPY . /kreate

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists
RUN pip3 install . && rm -rf /kreate
WORKDIR /