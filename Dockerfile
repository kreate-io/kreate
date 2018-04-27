FROM python:3.6.5-slim-stretch

ARG CLI_VERSION
ARG BUILD_DATE
ENV HELM_LATEST_VERSION="v2.9.0"
ENV KUBE_LATEST_VERSION="v1.9.6"

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

RUN apt-get update && apt-get install -y git wget \
    && wget http://storage.googleapis.com/kubernetes-helm/helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gz \
    && wget -O /usr/local/bin/kubectl https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl \
    && tar -xvf helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gz \
    && mv linux-amd64/helm /usr/local/bin \
    && chmod +x /usr/local/bin/kubectl \
    && rm -rf /var/cache/apk/* \
    && rm -f /helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gzrm -rf /var/lib/apt/lists

RUN pip3 install . && rm -rf /kreate
WORKDIR /
CMD bash