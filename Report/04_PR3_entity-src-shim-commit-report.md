# 04 — PR3 마지막 커밋 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 04 (PR3) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN`) |
| **대상 커밋** | **`f78949a`** — src/entity/ 실구현 추가 및 re-export shim·테스트 import 경로 정리 |
| 직전 커밋 | `c4fbfd8` — 루트 `entity/` 4파일 삭제 |
| Phase | GREEN (FR-01, FR-02 유지) |
| 상태 | Complete — `origin/GREEN` push 완료 |

---

## 1. Report 목적

본 Report는 **가장 마지막 커밋(`f78949a`)** 의 변경 범위·의도·영향을 문서화한다.

- `src/entity/` 실구현 추가 및 re-export shim 전환 내역을 기록한다.
- 테스트 import 경로 변경과 TC 회귀 여부를 확인한다.
- 직전 커밋(`c4fbfd8`)과의 관계를 PR3 관점에서 정리한다.
- 다음 GREEN 대상(FR-03~) 진입점을 제공한다.

---

## 2. 커밋 정보

### 2.1 HEAD — `f78949a`

| 항목 | 내용 |
|------|------|
| Hash | `f78949a20ac800322d8ab74f6c766c2ba4fd764b` |
| Author | usejen_id |
| Date | 2026-06-05 13:10:08 +0900 |
| Message | src/entity/ 실구현 추가 및 re-export shim·테스트 import 경로를 정리합니다. |

### 2.2 직전 커밋 — `c4fbfd8` (참고)

| 항목 | 내용 |
|------|------|
| Message | entity 패키지를 src/entity/로 통합하고 import 경로를 정리합니다. |
| 변경 | 루트 `entity/` 4파일 **삭제** (−61 lines) |

> PR3 push는 `c4fbfd8` → `f78949a` **2커밋**으로 구성. 본 Report의 **주 분석 대상**은 `f78949a`이며, `c4fbfd8`은 선행 삭제 커밋이다.

---

## 3. `f78949a` 변경 통계

| 항목 | 값 |
|------|-----|
| 변경 파일 | **13** |
| 삽입 | **+2,343** |
| 삭제 | **−52** |

> 삽입 대부분은 `Report/03_PR2_*` transcript(2,000 lines) 포함.

### 3.1 파일별 변경 목록

| 상태 | 경로 | 역할 |
|------|------|------|
| **A** | `src/entity/__init__.py` | entity 패키지 export |
| **A** | `src/entity/constants.py` | 변환 상수 SSOT |
| **A** | `src/entity/conversion_result.py` | `ConversionResult` DTO |
| **A** | `src/entity/registry.py` | `UnitRegistry` — meter 허브 |
| **M** | `src/constants.py` | → `src.entity.constants` re-export |
| **M** | `src/conversion_result.py` | → `src.entity.conversion_result` re-export |
| **M** | `src/registry.py` | → `src.entity.registry` re-export (37줄 → 3줄) |
| **M** | `src/converter.py` | import `src.entity.*` |
| **M** | `src/cli.py` | import `src.entity.registry` |
| **M** | `src/__init__.py` | docstring 갱신 |
| **M** | `tests/Domain/test_converter.py` | `src.entity.registry` import |
| **A** | `Report/03_PR2_entity-src-consolidation-report.md` | PR2 Report |
| **A** | `Report/03_PR2_entity-src-consolidation-report-transcript.md` | PR2 transcript |

---

## 4. 핵심 변경 내용

### 4.1 entity 실구현 → `src/entity/`

루트 `entity/`(c4fbfd8에서 삭제)의 역할을 **`src/entity/`** 로 이전·확정.

```
src/entity/
  constants.py         BASE_UNIT, FEET_PER_METER, YARD_PER_METER
  conversion_result.py   ConversionResult(unit, value)
  registry.py            UnitRegistry.default(), to_base(), from_base()
  __init__.py              public export
```

### 4.2 re-export shim (하위 호환)

| Shim 파일 | Before | After |
|-----------|--------|-------|
| `src/constants.py` | 상수 직접 정의 | `from src.entity.constants import ...` |
| `src/conversion_result.py` | DTO 직접 정의 | `from src.entity.conversion_result import ...` |
| `src/registry.py` | `UnitRegistry` 37줄 구현 | `from src.entity.registry import UnitRegistry` |

→ 기존 `from src.registry import UnitRegistry` import도 **동작 유지**.

### 4.3 Domain·CLI import 정렬

| 모듈 | 변경 import |
|------|-------------|
| `src/converter.py` | `src.entity.conversion_result`, `src.entity.registry` |
| `src/cli.py` | `src.entity.registry` |
| `tests/Domain/test_converter.py` | FR-02 GREEN TC: `src.entity.registry` |

---

## 5. 아키텍처 — 커밋 `f78949a` 이후

```
UnitConverter.py
  └── src/cli.py ──→ src/parser.py
                  ──→ src/entity/registry.py
                  ──→ src/converter.py ──→ src/entity/*

src/entity/          ← ECB entity SSOT (순수 도메인, I/O 없음)
src/converter.py     ← Domain 변환 (FR-02)
src/parser.py        ← Boundary 파싱 (FR-01)
src/registry.py      ← shim (하위 호환)
```

**의존 방향:** `cli/converter` → `entity` (단방향). `entity` → boundary/control import 없음.

---

## 6. TC 실행 결과 (커밋 `f78949a` 기준)

**명령:** `python -m pytest tests/ -v`

| # | Test ID | Req | Track | 결과 |
|---|---------|-----|-------|------|
| 1 | TC-FR-01 | FR-01 | UI | **PASS** |
| 2 | TC-FR-02 | FR-02 | Logic | **PASS** |
| 3 | U-FR-06 ~ U-FR-12 | FR-06~12 | UI | FAIL (RED) |
| 4 | D-FR-03 ~ D-FR-05 | FR-03~05 | Logic | FAIL (RED) |

**합계:** 13 collected — **2 passed, 11 failed**

> `f78949a`는 **구조 리팩터** 커밋. FR-01/FR-02 GREEN **회귀 없음**.

### 6.1 GREEN TC 확인 명령

```bash
python -m pytest tests/Boundary/test_cli.py::test_tc_fr_01_parse_meter_2_5 -v
python -m pytest tests/Domain/test_converter.py::test_tc_fr_02_convert_all_units_excluding_source -v
```

---

## 7. 커밋별 PR3 타임라인

```
521a4f4  FR-01/FR-02 GREEN + src 패키지 분리 (PR1)
    ↓
c4fbfd8  루트 entity/ 삭제                    (PR3-1)
    ↓
f78949a  src/entity/ 실구현 + shim + Report   (PR3-2) ← 본 Report 대상
    ↓
origin/GREEN push 완료
```

---

## 8. 미포함·후속 권장

| 항목 | 상태 |
|------|------|
| `src/formatter.py` (FR-03 반올림) | 미구현 — D-FR-03 RED |
| `src/validator.py` (FR-06~12) | 미구현 — U-FR-06~12 RED |
| `.gitignore` — `__pycache__/` | 미적용 (working tree에 pycache 잔존) |
| FR-11 TC 활성화 | parse_input strip 구현 있으나 TC RED |

### 8.1 PR4 제안 범위

| 순서 | 작업 | FR |
|------|------|-----|
| 1 | `src/formatter.py` + D-FR-03 GREEN | FR-03 |
| 2 | D-FR-04 TC 활성화 (Converter meter 허브) | FR-04 |
| 3 | `src/validator.py` + Boundary TC GREEN | FR-06~12 |

---

## 9. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| Report 02 | [Report/02_unit-converter-green-refactor-report.md](./02_unit-converter-green-refactor-report.md) |
| Report 03 (PR2 draft) | [Report/03_PR2_entity-src-consolidation-report.md](./03_PR2_entity-src-consolidation-report.md) |
| entity SSOT | [src/entity/](../src/entity/) |
| Cursor Rules | [.cursor/rules/.cursorrules](../.cursor/rules/.cursorrules) |
