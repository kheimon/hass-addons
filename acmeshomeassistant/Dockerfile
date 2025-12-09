ARG BUILD_FROM=ghcr.io/hassio-addons/base:stable
FROM ${BUILD_FROM}

RUN apk add --no-cache \
  openssl \
  openssh-client \
  coreutils \
  bind-tools \
  curl \
  sed \
  socat \
  tzdata \
  oath-toolkit-oathtool \
  tar \
  libidn \
  jq \
  ca-certificates \
  python3 \
  py3-pip

RUN curl https://get.acme.sh | sh
RUN ln -s /root/.acme.sh/acme.sh /usr/local/bin/acme.sh

RUN pip install --no-cache-dir "pydantic[email]>=2.12.4,<3.0"

COPY rootfs /