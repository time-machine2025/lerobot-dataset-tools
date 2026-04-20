from __future__ import annotations

from typing import List

from .schema import EpisodeRecord


def render_episode_timeline(episode: EpisodeRecord) -> str:
    lines: List[str] = [f"Episode: {episode.episode_id}", f"Task: {episode.task}", ""]
    for frame in episode.frames:
        lines.append(
            f"t={frame.t:02d} | action={frame.action:<5} | "
            f"agent={frame.agent} object={frame.object_pos} goal={frame.goal}"
        )
    return "\n".join(lines)
