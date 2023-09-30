## CS2 Server Docker

**WARNING:** This is in very early stages. Do not use unless you know what you're doing!

## Watchdog

Watchdog's job is to keep the server up to date. Whenever a new version is available, it hard links the game files into a new folder. Outdated versions that are no longer needed by any server get removed automatically.

### Environment

Currently the anonymous account can't download CS2.

- STEAM_USERNAME
- STEAM_PASSWORD

### Volumes

- `/repo` - Everything that's meant to persist. Server files, steamcmd, etc.
- `/hooks` - Contains `hooks.py` and your other python dependencies.

### Hooks

This is an example `hooks.py` from `/hooks`. 

```Py
def post_update(version: int, dir: str) -> None:
    print("The server updated to", version)
```

## Server

### Volumes

- `/repo` - This is meant to be shared with the watchdog.
- `/hooks` - Contains `hooks.py` and your other python dependencies.

### Hooks

This is an example `hooks.py` from `/hooks`. 

```Py
def post_build(version: int, dir: str) -> None:
    pass

def pre_run(version: int, dir: str, args: list[str]) -> None:
    args.append('+hostname cs2-server-docker')
    args.append('+map de_inferno')
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

# Fill in STEAM_USERNAME and STEAM_PASSWORD with a throwaway account that has CS2 added to their library.
# I'd recommend disabling steam guard to avoid issues.
nano docker-compose.yml
```
