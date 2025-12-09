ARG BUILD_FROM
FROM $BUILD_FROM

# install prerequisites to container
RUN apk add --no-cache \
  openssl \
  openssh-client \
  ca-certificates \
  coreutils \
  bind-tools \
  curl \
  sed \
  socat \
  tzdata \
  oath-toolkit-oathtool \
  tar \
  libidn

# Install acme.sh from online sources without enabling cron
RUN curl https://get.acme.sh | sh --install --no-cron
RUN ln -s /root/.acme.sh/acme.sh /usr/local/bin/acme.sh

COPY run.sh /run.sh
RUN chmod a+x /run.sh

ENTRYPOINT [ "/run.sh" ]
