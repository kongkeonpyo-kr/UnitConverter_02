"""
tests/test_config_loader.py — EXT 설정 외부화 (P1) 테스트

PRD 추적
--------
- 문서   : PRD/unit-converter-prd.md
- §3.5   : EXT-01 ~ EXT-04 설정 파일 로드
- §8.4   : TC-EXT-01 ~ TC-EXT-04
- Track  : Logic (Domain — Registry·config)
- Test File : tests/test_config_loader.py
"""

import pytest

from tests.conftest import FIXTURE_UNITS_PATH


# ---------------------------------------------------------------------------
# Req ID  : EXT-01
# Track   : Logic
# Test ID : D-EXT-01 / TC-EXT-01
# Layer   : entity
# P       : P1
# Given   : tests/fixtures/units.json (TC 전용, 사용자 config 와 분리)
# Then    : feet=3.0, yard=1.0, meter=1.0 로드
# ---------------------------------------------------------------------------
@pytest.mark.req("EXT-01")
@pytest.mark.track("Logic")
def test_d_ext01_load_units_json():
    """D-EXT-01 / TC-EXT-01: units.json 비율 로드 — EXT-01"""
    from src.config_loader import load_units

    # Act (GREEN)
    units = load_units(FIXTURE_UNITS_PATH)

    # Assert
    assert units["meter"] == 1.0
    assert units["feet"] == 3.0
    assert units["yard"] == 1.0


# ---------------------------------------------------------------------------
# Req ID  : EXT-01
# Track   : Logic
# Test ID : D-EXT-01b / TC-EXT-01 (변환 연동)
# Layer   : entity
# P       : P1
# Given   : tests/fixtures/units.json 로드 Registry
# Then    : meter:2.5 → feet·yard 변환 (로드 비율 사용)
# ---------------------------------------------------------------------------
@pytest.mark.req("EXT-01")
@pytest.mark.track("Logic")
def test_d_ext01_convert_using_loaded_units_config():
    """D-EXT-01b: 로드한 비율로 변환 — EXT-01 (Logic Track)"""
    from src.config_loader import load_unit_registry
    from src.converter import Converter

    # Arrange
    registry = load_unit_registry(FIXTURE_UNITS_PATH)
    converter = Converter(registry)
    source_unit = "meter"
    value = 2.5
    tolerance = 1e-4

    # Act (GREEN)
    results = converter.convert(source_unit, value)

    # Assert — 소스 제외, config 비율로 변환
    feet = next(r for r in results if r.unit == "feet")
    yard = next(r for r in results if r.unit == "yard")
    assert abs(feet.value - (value * 3.0)) < tolerance
    assert abs(yard.value - (value * 1.0)) < tolerance
