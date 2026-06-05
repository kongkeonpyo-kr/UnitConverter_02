"""Golden master expected 출력 파일 생성 (리팩토링 전 1회 또는 의도적 변경 후)."""

import contextlib
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import src.config_loader as config_loader
from src.cli import run

CASES = ROOT / "golden_master" / "cases.json"
OUT_DIR = ROOT / "golden_master" / "expected"
# Golden baseline = TC fixture (사용자 config/units.json 과 무관)
FIXTURE_UNITS_PATH = ROOT / "tests" / "fixtures" / "units.json"


def capture(input_str: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        run(input_str)
    return buf.getvalue()


def main() -> None:
    config_loader.default_config_path = lambda: FIXTURE_UNITS_PATH
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    for case in cases:
        output = capture(case["input"])
        path = OUT_DIR / f"{case['id']}.txt"
        path.write_text(output, encoding="utf-8", newline="\n")
        print(f"written: {path}")


if __name__ == "__main__":
    main()
