from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

ALLOWED_ACTIONS = {"up", "down", "left", "right", "pick", "place"}


@dataclass(frozen=True)
class Frame:
    t: int
    agent: tuple[int, int]
    object_pos: tuple[int, int]
    goal: tuple[int, int]
    action: str


@dataclass(frozen=True)
class EpisodeRecord:
    episode_id: str
    task: str
    frames: tuple[Frame, ...]


def validate_episode(payload: dict) -> List[str]:
    errors: List[str] = []
    if not isinstance(payload.get("episode_id"), str):
        errors.append("episode_id must be a string")
    if not isinstance(payload.get("task"), str):
        errors.append("task must be a string")
    frames = payload.get("frames")
    if not isinstance(frames, list) or not frames:
        errors.append("frames must be a non-empty list")
        return errors

    previous_t = -1
    for idx, frame in enumerate(frames):
        prefix = f"frame[{idx}]"
        if not isinstance(frame.get("t"), int):
            errors.append(f"{prefix}.t must be an int")
        elif frame["t"] <= previous_t:
            errors.append(f"{prefix}.t must be strictly increasing")
        else:
            previous_t = frame["t"]

        for key in ("agent", "object", "goal"):
            value = frame.get(key)
            if not isinstance(value, list) or len(value) != 2 or not all(isinstance(item, int) for item in value):
                errors.append(f"{prefix}.{key} must be a pair of ints")
        action = frame.get("action")
        if action not in ALLOWED_ACTIONS:
            errors.append(f"{prefix}.action must be one of {sorted(ALLOWED_ACTIONS)}")
    return errors


def build_episode(payload: dict) -> EpisodeRecord:
    return EpisodeRecord(
        episode_id=payload["episode_id"],
        task=payload["task"],
        frames=tuple(
            Frame(
                t=frame["t"],
                agent=tuple(frame["agent"]),
                object_pos=tuple(frame["object"]),
                goal=tuple(frame["goal"]),
                action=frame["action"],
            )
            for frame in payload["frames"]
        ),
    )


def validate_many(items: Iterable[dict]) -> List[str]:
    errors: List[str] = []
    seen_ids: set[str] = set()
    for idx, payload in enumerate(items):
        episode_errors = validate_episode(payload)
        errors.extend(f"episode[{idx}]: {message}" for message in episode_errors)
        episode_id = payload.get("episode_id")
        if isinstance(episode_id, str):
            if episode_id in seen_ids:
                errors.append(f"episode[{idx}]: duplicate episode_id {episode_id}")
            seen_ids.add(episode_id)
    return errors
