FROM python:3.6.4-alpine

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

WORKDIR kreate-cli
COPY . /kreate-cli

RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --update add --no-cache \ 
    lapack-dev \ 
    gcc \
    freetype-dev

# Install dependencies
RUN apk add --no-cache --virtual .build-deps \
    musl-dev \
    g++
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install .

# removing dependencies
RUN apk del .build-deps

WORKDIR /
CMD bash