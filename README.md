# LeRobot Dataset Tools

This repository contains lightweight utilities for embodied robotics datasets:

- schema validation
- dataset statistics
- task vocabulary summaries
- episode timeline rendering

The implementation is intentionally small and dependency-light so it is easy to review in an application setting.

## Why It Exists

Many embodied AI projects become difficult to debug long before model training because the dataset layer is messy. This repository focuses on the unglamorous but important work of making trajectory data inspectable and reliable.

## Quick Start

```bash
python3 scripts/dataset_cli.py validate data/sample_dataset.jsonl
python3 scripts/dataset_cli.py stats data/sample_dataset.jsonl
python3 scripts/dataset_cli.py render data/sample_dataset.jsonl --episode episode-002
```

Requirements:

- Python 3.10+
- no third-party dependencies for the current CLI

Example statistics output:

```json
{
  "num_episodes": 3,
  "avg_episode_length": 8.33,
  "task_distribution": {
    "pick red block to left goal": 1,
    "pick blue cup to right tray": 1,
    "pick green bottle to top shelf": 1
  }
}
```

## Tooling Scope

- `validate`: schema checks and duplicate ID detection
- `stats`: dataset-level summaries for task and action balance
- `render`: a quick textual episode viewer for inspection and debugging

## Minimal Verification

```bash
python3 -m unittest discover -s tests -q
```

