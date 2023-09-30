FROM debian:bookworm-slim

RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        wget \
        python3 \
        python3-requests \
        lib32gcc-s1

ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o "watchdog" \
    && useradd -u $UID -g $GID -o "watchdog" \
    && mkdir /app \
    && mkdir /app/steamcmd \
    && mkdir /hooks \
    && mkdir /repo \
    && chown watchdog:watchdog /repo
    
COPY start.py /app
RUN wget -qO- 'http://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' | tar xvz -C /app/steamcmd

COPY hooks.py /hooks
ENV PYTHONPATH "/hooks:${PYTHONPATH}"

USER watchdog
CMD [ "python3", "/app/start.py" ]
