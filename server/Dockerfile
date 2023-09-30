FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        python3 \
        python3-requests

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o "server" \
    && useradd -u $UID -g $GID -m -o "server" \
    && mkdir /hooks \
    && mkdir /app

COPY start.py /app

COPY hooks.py /hooks
ENV PYTHONPATH "/hooks:${PYTHONPATH}"

USER server
CMD [ "python3", "/app/start.py" ]
