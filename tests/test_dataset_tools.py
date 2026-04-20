from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lerobot_dataset_tools.io import load_dataset, load_payloads
from lerobot_dataset_tools.schema import validate_many
from lerobot_dataset_tools.stats import summarize_dataset


class DatasetToolsTest(unittest.TestCase):
    def test_sample_dataset_is_valid_and_has_stats(self) -> None:
        payloads = load_payloads(ROOT / "data" / "sample_dataset.jsonl")
        self.assertEqual(validate_many(payloads), [])
        summary = summarize_dataset(load_dataset(ROOT / "data" / "sample_dataset.jsonl"))
        self.assertEqual(summary["num_episodes"], 3)
        self.assertIn("pick", summary["action_histogram"])


if __name__ == "__main__":
    unittest.main()
