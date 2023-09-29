import signal
import os
import sys
import subprocess
import shutil
import time
import pathlib
import user
import requests
from requests.exceptions import RequestException

def signal_handler(sig, frame):
    sys.exit(0)
signal.signal(signal.SIGTERM, signal_handler)

SERVERS_DIR: str = '/repo/servers'
INSTALL_DIR: str = os.path.join(SERVERS_DIR, 'latest')
STEAMCMD_DIR: str = '/repo/steamcmd'
STEAMCMD_INITIAL_DIR: str = '/home/steam/steamcmd'
STEAMCMD_PATH: str = os.path.join(STEAMCMD_DIR, 'steamcmd.sh')
LOCK_FILE_NAME: str = 'watchdog.lock'
STEAM_USERNAME: str = str(os.environ.get('STEAM_USERNAME'))
STEAM_PASSWORD: str = str(os.environ.get('STEAM_PASSWORD'))

def fetch_latest_version() -> int:
    response = requests.get('https://api.steampowered.com/ISteamApps/UpToDateCheck/v1?version=0&format=json&appid=730')
    if response.status_code != 200:
        raise RequestException('steam api response status is not 200')
    response = response.json()
    response = response['response']
    if not response['success']:
        raise RequestException('steam api response says it failed')
    return int(response['required_version'])

def collect_installed_versions() -> list[int]:
    versions: list[int] = []
    for it in os.listdir(SERVERS_DIR):
        if it.isdigit() and os.path.isdir(os.path.join(SERVERS_DIR, it)):
            versions.append(int(it))
    return versions

def delete_unused_versions() -> None:
    installed_versions: list[int] = collect_installed_versions()
    latest_installed_version: int = max(installed_versions, default=0)
    for version in installed_versions:
        if version == latest_installed_version:
            continue
        lock_file_path: str = os.path.join(SERVERS_DIR, str(version), LOCK_FILE_NAME)
        lock_file_exists: bool = os.path.isfile(lock_file_path)
        if lock_file_exists:
            try:
                os.remove(lock_file_path)
            except:
                continue
        shutil.rmtree(os.path.join(SERVERS_DIR, str(version)))

def link_dir(source: str, target: str) -> None:
    if os.path.lexists(target):
        if os.path.isfile(target) or os.path.islink(target):
            os.remove(target)
        elif os.path.isdir(target):
            shutil.rmtree(target)
    for root, _, files in os.walk(source):
        root_relative: str = os.path.relpath(root, source)
        if root_relative == '.':
            root_relative = '' # why?
        os.mkdir(os.path.join(target, root_relative))
        for filename in files:
            source_file = os.path.join(root, filename)
            target_file = os.path.join(target, root_relative, filename)
            os.link(source_file, target_file)

def update_if_needed() -> None:
    latest_version: int = fetch_latest_version()
    installed_versions: list[int] = collect_installed_versions()
    if len(installed_versions) != 0:
        latest_installed_version: int = max(installed_versions)
        if latest_installed_version == latest_version:
            lock_file_path: str = os.path.join(SERVERS_DIR, str(latest_version), LOCK_FILE_NAME)
            if os.path.exists(lock_file_path):
                return
    # Technically this can download a version different than 'latest_version' and we'd never know
    steamcmd_result = subprocess.run([
        STEAMCMD_PATH, 
        '+@ShutdownOnFailedCommand', '1',
        '+@NoPromptForPassword', '1',
        '+@bMetricsEnabled', '0',
        '+force_install_dir', INSTALL_DIR,
        '+login', STEAM_USERNAME, STEAM_PASSWORD,
        '+app_update', '730',# 'validate',
        '+quit'
    ])
    if steamcmd_result.returncode == 0:
        version_dir: str = os.path.join(SERVERS_DIR, str(latest_version))
        link_dir(INSTALL_DIR, version_dir)
        try:
            user.post_update(version=latest_version, dir=version_dir)
        except:
            pass
        lock_file_path: str = os.path.join(version_dir, LOCK_FILE_NAME)
        pathlib.Path(lock_file_path).touch()

def main() -> None:
    if not os.path.exists(STEAMCMD_PATH):
        shutil.copytree(STEAMCMD_INITIAL_DIR, STEAMCMD_DIR, dirs_exist_ok=True)

    while True:
        update_if_needed()
        delete_unused_versions()
        time.sleep(60)

if __name__ == '__main__':
    main()
