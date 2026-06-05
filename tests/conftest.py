"""pytest 공통 설정 — TC는 사용자 config/units.json 과 분리된 fixture 사용."""

from pathlib import Path

import pytest

TESTS_ROOT = Path(__file__).resolve().parent
FIXTURE_UNITS_PATH = TESTS_ROOT / "fixtures" / "units.json"


@pytest.fixture(autouse=True)
def isolate_units_config_from_user_file(monkeypatch):
    """사용자가 수정한 config/units.json 이 TC·Golden Master에 영향 주지 않도록 고정."""
    monkeypatch.setattr(
        "src.config_loader.default_config_path",
        lambda: FIXTURE_UNITS_PATH,
    )
