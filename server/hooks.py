
def post_build(version: int, dir: str) -> None:
    pass

def pre_run(version: int, dir: str, args: list[str]) -> None:
    server_name = os.environ.get("SERVER_NAME", "Counter-Strike 2 Dedicated Server")
    map_name = os.environ.get("MAP", "de_inferno")
    server_pw = os.environ.get("SERVER_PW", "")  # Set default value if not provided
    rcon_pw = os.environ.get("RCON_PW", "12345")  # Set default value if not provided
    port = os.environ.get("PORT", "27015")  # Set default value if not provided
    game_type = os.environ.get("GAME_TYPE", "0")  # Set default value if not provided
    game_mode = os.environ.get("GAME_MODE", "1")  # Set default value if not provided
    max_players = os.environ.get("MAX_PLAYERS", "10")  # Set default value if not provided

    args.append(f"+hostname {server_name}")
    args.append(f"+map {map_name}")
    args.append(f"+sv_password {server_pw}")
    args.append(f"+rcon_password {rcon_pw}")
    args.append(f"-port {port}")
    args.append(f"+gamemode {game_mode}")
    args.append(f"+game_type {game_type}")
    args.append(f"-maxplayers {max_players}")
