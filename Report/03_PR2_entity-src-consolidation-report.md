# 03 — PR2 entity → src/entity 통합 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 03 (PR2) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `521a4f4` — FR-01/FR-02 GREEN + src 패키지 분리 |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN (FR-01, FR-02 유지) |
| PR | PR2 — entity 레이어 `src/entity/` 통합 |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 PR2 작업으로 **루트 `entity/` 패키지를 `src/entity/`로 통합**한 변경분을 `git status` 기준으로 기록한다.

- Report 02에서 지적된 **`entity/` vs `src/` 중복·미연동** 문제 해소 내역을 문서화한다.
- ECB entity 레이어의 단일 위치(`src/entity/`)를 확정한다.
- 하위 호환 re-export shim 및 import 경로 변경을 추적한다.
- TC 통과 현황(GREEN/RED) 스냅샷을 PR2 리뷰 자료로 제공한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes to be committed:
  deleted:    entity/__init__.py
  deleted:    entity/constants.py
  deleted:    entity/conversion_result.py
  deleted:    entity/registry.py

Changes not staged for commit:
  modified:   src/__init__.py
  modified:   src/cli.py
  modified:   src/constants.py
  modified:   src/conversion_result.py
  modified:   src/converter.py
  modified:   src/registry.py
  modified:   tests/Domain/test_converter.py
  modified:   src/__pycache__/*.pyc   (커밋 제외 권장)

Untracked files:
  src/entity/            (신규 — entity 실구현)
  boundary/              (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 Diff 통계

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| Staged (삭제) | `entity/` 4파일 | 0 | −61 |
| Unstaged (수정) | `src/` 6파일, `tests/` 1파일 | +13 | −52 |
| Untracked (신규) | `src/entity/` 4파일 | +61 (상당) | — |

---

## 3. 변경 요약 — PR2 핵심

| Before (521a4f4) | After (working tree) |
|------------------|----------------------|
| `entity/` (루트, 미연동) + `src/` (동일 로직 중복) | `src/entity/` (단일 SSOT) |
| `src/registry.py` 등에 entity 로직 직접 구현 | `src/registry.py` 등 → **re-export shim** |
| 테스트: `from src.registry import UnitRegistry` | 테스트: `from src.entity.registry import UnitRegistry` |

---

## 4. 변경 파일 상세

### 4.1 삭제 (Staged) — 루트 `entity/`

| 파일 | 역할 | 이전 상태 |
|------|------|-----------|
| `entity/__init__.py` | entity 패키지 export | `521a4f4`에 커밋됐으나 미연동 |
| `entity/constants.py` | 변환 상수 SSOT | `src/constants.py`와 중복 |
| `entity/conversion_result.py` | `ConversionResult` DTO | `src/conversion_result.py`와 중복 |
| `entity/registry.py` | `UnitRegistry` | `src/registry.py`와 중복 |

### 4.2 신규 (Untracked) — `src/entity/`

| 파일 | Layer | 역할 |
|------|-------|------|
| `src/entity/__init__.py` | entity | 패키지 export |
| `src/entity/constants.py` | entity | `BASE_UNIT`, `FEET_PER_METER`, `YARD_PER_METER` |
| `src/entity/conversion_result.py` | entity | `ConversionResult` dataclass |
| `src/entity/registry.py` | entity | `UnitRegistry` — meter 허브·OCP |

### 4.3 수정 (Unstaged) — `src/` re-export 및 import 정렬

#### `src/constants.py`

```diff
- BASE_UNIT = "meter"  (직접 정의)
+ from src.entity.constants import BASE_UNIT, FEET_PER_METER, YARD_PER_METER
```

#### `src/conversion_result.py`

```diff
- class ConversionResult: ...  (직접 정의)
+ from src.entity.conversion_result import ConversionResult
```

#### `src/registry.py`

```diff
- class UnitRegistry: ...  (37줄 직접 구현)
+ from src.entity.registry import UnitRegistry
```

#### `src/converter.py`

```diff
- from src.conversion_result import ConversionResult
- from src.registry import UnitRegistry
+ from src.entity.conversion_result import ConversionResult
+ from src.entity.registry import UnitRegistry
```

#### `src/cli.py`

```diff
- from src.registry import UnitRegistry
+ from src.entity.registry import UnitRegistry
```

#### `src/__init__.py`

- docstring: `entity, parser, converter, cli` 명시

### 4.4 수정 (Unstaged) — 테스트

#### `tests/Domain/test_converter.py`

| 위치 | 변경 |
|------|------|
| `test_tc_fr_02_*` (FR-02 GREEN) | `src.registry` → `src.entity.registry` |
| `test_d_fr04_*`, `test_d_fr05_*` (RED 주석) | 동일 import 경로 갱신 |

> `tests/Boundary/test_cli.py` — PR2에서 **변경 없음**

---

## 5. 아키텍처 — PR2 이후 `src/` 구조

```
src/
  entity/                  ← ECB entity (실구현 SSOT)
    constants.py
    conversion_result.py
    registry.py
  parsed_input.py          ← Boundary DTO
  parser.py                ← Boundary — FR-01
  converter.py             ← Domain — FR-02 (entity 의존)
  cli.py                   ← Boundary — CLI
  constants.py             ← shim (하위 호환)
  conversion_result.py     ← shim
  registry.py              ← shim
UnitConverter.py           ← src.cli 위임 (변경 없음)
```

**의존 방향**

```
cli ──→ parser, entity.registry, converter
converter ──→ entity.conversion_result, entity.registry
entity.* ──→ (stdlib only, I/O 없음)
```

---

## 6. Report 02 대비 해소 항목

| Report 02 지적 | PR2 조치 |
|----------------|----------|
| `entity/` vs `src/` 중복 | ✅ `entity/` 삭제, `src/entity/` 단일화 |
| entity 미연동 | ✅ `converter`, `cli`, 테스트가 `src.entity.*` 참조 |
| 커밋 시 중복 검토 필요 | ✅ re-export shim으로 기존 `src.registry` import도 유지 가능 |

---

## 7. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

| # | Test ID | Req | Track | 결과 |
|---|---------|-----|-------|------|
| 1 | TC-FR-01 | FR-01 | UI | **PASS** |
| 2 | U-FR-06 ~ U-FR-12 | FR-06~12 | UI | FAIL (RED) |
| 3 | TC-FR-02 | FR-02 | Logic | **PASS** |
| 4 | D-FR-03 ~ D-FR-05 | FR-03~05 | Logic | FAIL (RED) |

**합계:** 13 collected — **2 passed, 11 failed**

> PR2는 **구조 리팩터**이며 FR-01/FR-02 GREEN 회귀 없음.

### 7.1 GREEN TC 실행 명령

```bash
python -m pytest tests/Boundary/test_cli.py::test_tc_fr_01_parse_meter_2_5 -v
python -m pytest tests/Domain/test_converter.py::test_tc_fr_02_convert_all_units_excluding_source -v
```

---

## 8. 커밋 권장 사항 (PR2)

### 8.1 포함 권장

```
entity/          (삭제 — staged)
src/entity/      (신규 4파일)
src/__init__.py
src/cli.py
src/constants.py
src/conversion_result.py
src/converter.py
src/registry.py
tests/Domain/test_converter.py
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (소스 없음)
- `src/__pycache__/*.pyc` (이전 커밋에 포함됐다면 별도 `.gitignore` 정리 PR 권장)

### 8.3 제안 커밋 메시지

```
entity 패키지를 src/entity/로 통합하고 import 경로를 정리합니다.
```

### 8.4 PR2 제안 제목

```
PR2: entity → src/entity 통합 및 ECB 레이어 정렬
```

---

## 9. 다음 단계 (PR3 이후)

| 순서 | 작업 | 대상 FR |
|------|------|---------|
| 1 | `src/validator.py` GREEN | FR-06~12 |
| 2 | FR-11 TC 활성화 (parse_input strip 이미 구현) | FR-11 |
| 3 | `src/formatter.py` GREEN | FR-03, FR-05 |
| 4 | D-FR-04 TC 활성화 (Converter 이미 meter 허브) | FR-04 |
| 5 | `.gitignore` — `__pycache__/` | — |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| Report 01 | [Report/01_unit-converter-prd-report.md](./01_unit-converter-prd-report.md) |
| Report 02 | [Report/02_unit-converter-green-refactor-report.md](./02_unit-converter-green-refactor-report.md) |
| entity (신규) | [src/entity/](../src/entity/) |
| Cursor Rules | [.cursor/rules/.cursorrules](../.cursor/rules/.cursorrules) |
