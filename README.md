## CS2 Server Docker

**WARNING:** This is in very early stages. Do not use unless you know what you're doing!

## Watchdog

### Environment

Currently the anonymous account can't download CS2.

- STEAM_USERNAME
- STEAM_PASSWORD

### Volumes

- `/repo` - Everything that's meant to persist. Server files, steamcmd, etc.

### Hooks

Override the `/scripts/user.py` file in the container to access hooks.

```Py
def post_update(version: int, dir: str) -> None:
    print("The server updated to", version)
```

## Server

At the moment it just starts a default server on Inferno.

### Volumes

- `/repo` - This is meant to be shared with the watchdog.

### Hooks

Override the `/scripts/user.py` file in the container to access hooks.

```Py
def post_build(version: int, dir: str) -> None:
    print("The server was just built")
```

## Recommended setup

```bash
WATCHDOG_IDS=5000
SERVER_IDS=5001

sudo groupadd -g $WATCHDOG_IDS cs2-watchdog
sudo useradd -u $WATCHDOG_IDS -g $WATCHDOG_IDS -M -s /bin/false cs2-watchdog
sudo groupadd -g $SERVER_IDS cs2-server
sudo useradd -u $SERVER_IDS -g $SERVER_IDS -M -s /bin/false cs2-server

cd ~
mkdir gameservers
cd gameservers

git clone https://github.com/Szwagi/cs2-server-docker.git images

cp images/example-docker-compose.yml docker-compose.yml

mkdir repo
chgrp watchdog repo
chmod g+s repo

mkdir -p hooks/watchdog
mkdir -p hooks/server
cp images/watchdog/hooks.py hooks/watchdog
cp images/server/hooks.py hooks/server

docker build --build-arg UID=$WATCHDOG_IDS --build-arg GID=$WATCHDOG_IDS -t cs2-watchdog images/watchdog
docker build --build-arg UID=$SERVER_IDS --build-arg GID=$SERVER_IDS -t cs2-server images/server
```
