FROM python:3.9-alpine


# Defining the workdir
#=======================================================================================================================
WORKDIR /app


# Copying needed files
#=======================================================================================================================
COPY lbz2twitter lbz2twitter
COPY config config
COPY scripts/run.sh .


# Installation of packages
#=======================================================================================================================
RUN apk add --update --no-cache curl && \
    pip install --no-cache-dir -r /app/lbz2twitter/python-deps.txt && \
    rm -f /app/lbz2twitter/python-deps.txt

# Required by the locales
ENV MUSL_LOCPATH="/usr/share/i18n/locales/musl"
RUN apk --no-cache --update add \
    musl-locales \
    musl-locales-lang

# Supercronic installation
#-------------------------
ARG SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.12/supercronic-linux-amd64
ARG SUPERCRONIC=supercronic-linux-amd64
ARG SUPERCRONIC_SHA1SUM=048b95b48b708983effb2e5c935a1ef8483d9e3e

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN curl -fsSLO "$SUPERCRONIC_URL" && \
    echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - && \
    chmod +x "$SUPERCRONIC" && \
    mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" && \
    ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic


# Environment variables
#=======================================================================================================================

# Env. variables for script customization
#----------------------------------------
ENV UID=1000 \
    GID=1000 \
    DEBUG=False \
    LB_USER="" \
    LB_FETCH=10 \
    LB_VERIFIED=3 \
    DL_RETRIES=5 \
    DL_DELAY=5 \
    LOCALE="es_ES.UTF-8" \
    TW_CONSUMER_KEY="" \
    TW_CONSUMER_SECRET="" \
    TW_ACCESS_TOKEN="" \
    TW_ACCESS_TOKEN_SECRET="" \
    TW_RETRIES=5 \
    TW_DELAY=5 \
    TW_HOUR=20


# Creation of appuser and giving proper permissions to files and dirs
#=======================================================================================================================
RUN addgroup -g $GID appuser && \
    adduser -D -u $UID -G appuser appuser && \
    chown -R appuser:appuser /app && \
    chmod 500 /app/lbz2twitter/lbz2twitter.py && \
    chmod 500 /app/run.sh


# Running the container
#=======================================================================================================================
USER appuser
CMD ["/app/run.sh"]