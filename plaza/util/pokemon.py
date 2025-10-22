import json
from pathlib import Path

pwd = Path(__file__).parent

with open(pwd / "pokemon_db.json") as f:
    pokemon_db: dict[int, dict[str, str | list]] = {
        int(k): v
        for k, v in json.loads(f.read()).items()
    }

VALID_MONS = list(pokemon_db.keys())
