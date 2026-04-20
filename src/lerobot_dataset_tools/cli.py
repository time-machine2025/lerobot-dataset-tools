from __future__ import annotations

import argparse
import json

from .io import load_dataset, load_payloads
from .schema import validate_many
from .stats import summarize_dataset
from .visualize import render_episode_timeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Dataset tools for embodied episodes.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("path")

    stats_parser = subparsers.add_parser("stats")
    stats_parser.add_argument("path")

    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("path")
    render_parser.add_argument("--episode", required=True)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "validate":
        payloads = load_payloads(args.path)
        errors = validate_many(payloads)
        if errors:
            print("INVALID")
            for error in errors:
                print("-", error)
            raise SystemExit(1)
        print("VALID")
        return

    if args.command == "stats":
        summary = summarize_dataset(load_dataset(args.path))
        print(json.dumps(summary, indent=2))
        return

    dataset = load_dataset(args.path)
    episode = next((item for item in dataset if item.episode_id == args.episode), None)
    if episode is None:
        raise SystemExit(f"Episode not found: {args.episode}")
    print(render_episode_timeline(episode))


if __name__ == "__main__":
    main()
