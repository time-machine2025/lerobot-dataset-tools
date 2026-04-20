from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .schema import EpisodeRecord, build_episode


def load_payloads(path: str | Path) -> List[dict]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_dataset(path: str | Path) -> List[EpisodeRecord]:
    return [build_episode(item) for item in load_payloads(path)]
