FROM debian:bookworm-slim

RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        wget \
        python3 \
        python3-requests \
        lib32gcc-s1

ENV PUID 1000
RUN useradd -u "${PUID}" -m "steam"

RUN mkdir -p -m700 /steamcmd \
    && mkdir -p -m700 /repo \
    && chown steam:steam /steamcmd /repo

USER steam
WORKDIR /home/steam

RUN ln -s /user.py user.py \
    && mkdir steamcmd \
    && wget -qO- 'http://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz' | tar xvz -C steamcmd

COPY script.py .
COPY user.py /

CMD [ "python3", "script.py" ]
