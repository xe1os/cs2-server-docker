FROM debian:bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
        python3 \
        python3-requests

ENV PUID 1000
RUN useradd -u "${PUID}" -m "server"

USER server
WORKDIR /home/server

RUN ln -s /user.py user.py

COPY script.py .
COPY user.py /

CMD [ "python3", "script.py" ]
