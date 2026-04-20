from __future__ import annotations

from collections import Counter
from typing import Dict, Iterable

from .schema import EpisodeRecord


def summarize_dataset(episodes: Iterable[EpisodeRecord]) -> Dict[str, object]:
    episode_list = list(episodes)
    action_counter: Counter[str] = Counter()
    task_counter: Counter[str] = Counter()
    lengths = []
    vocabulary: Counter[str] = Counter()

    for episode in episode_list:
        task_counter[episode.task] += 1
        lengths.append(len(episode.frames))
        vocabulary.update(word.lower() for word in episode.task.replace("-", " ").split())
        for frame in episode.frames:
            action_counter[frame.action] += 1

    avg_length = sum(lengths) / len(lengths) if lengths else 0.0
    return {
        "num_episodes": len(episode_list),
        "avg_episode_length": round(avg_length, 2),
        "task_distribution": dict(task_counter),
        "action_histogram": dict(action_counter),
        "top_task_words": vocabulary.most_common(8),
    }
