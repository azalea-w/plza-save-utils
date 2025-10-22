import json
from pathlib import Path

from ..types.bagsave import CategoryType

pwd = Path(__file__).parent

with open(pwd / "item_db.json") as f:
    item_db: dict[int, dict[str, str | int | CategoryType]] = {
        int(k): v | {"expected_category": CategoryType(v["expected_category"])}
        for k, v in json.loads(f.read()).items()
    }

VALID_ITEMS = list(item_db.keys())
