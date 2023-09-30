
def post_build(version: int, dir: str) -> None:
    pass

def pre_run(version: int, dir: str, args: list[str]) -> None:
    args.append('+hostname cs2-server-docker')
    args.append('+map de_inferno')
