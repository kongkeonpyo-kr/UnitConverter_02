import json
from pathlib import Path

from src.entity.registry import UnitRegistry


def default_config_path() -> Path:
    """기본 단위 설정 파일 경로 — config/units.json."""
    return Path(__file__).resolve().parents[1] / "config" / "units.json"


def load_units(path: Path | str) -> dict[str, float]:
    """JSON 설정 파일에서 unit→meter 비율 dict를 로드한다 (EXT-01)."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    return {name: float(ratio) for name, ratio in raw.items()}


def load_unit_registry(path: Path | str) -> UnitRegistry:
    """설정 파일 비율로 UnitRegistry를 생성한다 (EXT-01)."""
    return UnitRegistry(load_units(path))


__all__ = ["default_config_path", "load_units", "load_unit_registry"]
