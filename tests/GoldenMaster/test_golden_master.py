"""Golden master — cli.run() stdout 스냅샷 회귀 검증."""

import contextlib
import io
import json
from pathlib import Path

import pytest

from src.cli import run

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "golden_master" / "cases.json"
EXPECTED_DIR = ROOT / "golden_master" / "expected"


def _capture(input_str: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run(input_str)
    return buf.getvalue()


def _load_cases():
    return json.loads(CASES.read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])
def test_golden_master(case):
    expected_path = EXPECTED_DIR / f"{case['id']}.txt"
    assert expected_path.exists(), f"missing golden file: {expected_path}"

    expected = expected_path.read_text(encoding="utf-8")
    actual = _capture(case["input"])

    assert actual == expected, (
        f"golden master mismatch: {case['id']}\n"
        f"--- expected ---\n{expected!r}\n"
        f"--- actual ---\n{actual!r}"
    )
