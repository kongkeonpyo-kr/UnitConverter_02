# 02 — Unit Converter GREEN 리팩터링 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 02 |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `0dc5ecb` — 테스트 Boundary/Domain 폴더 재배치 |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN (FR-01, FR-02 부분 통과) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 `git status`를 기준으로 **현재 작업 트리에 존재하는 수정·신규 파일**을 목록화하고, 레거시 `UnitConverter.py`의 `src/` 분리 리팩터링 내용을 기록한다.

- 변경 파일별 역할·의존 관계를 파악할 수 있도록 한다.
- 레거시 단일 `main()` → 모듈 분리 매핑을 문서화한다.
- TC(GREEN/RED) 통과 현황을 스냅샷으로 남긴다.
- 커밋·PR 작성 전 변경 범위 검토 자료로 활용한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   UnitConverter.py
  modified:   tests/Boundary/test_cli.py

Untracked files:
  boundary/          (__pycache__ 잔존만 — .py 소스 없음)
  entity/            (ECB entity 초안 — src와 미연동)
  src/               (신규 구현 패키지)
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (staged + unstaged)

| 구분 | 파일 수 | 삽입 | 삭제 |
|------|---------|------|------|
| 수정 (tracked) | 2 | +11 | −40 |
| 신규 (untracked) | `src/` 8파일, `entity/` 4파일 | — | — |

---

## 3. 변경 파일 상세

### 3.1 수정됨 (Modified)

#### `UnitConverter.py`

| 항목 | 내용 |
|------|------|
| 변경 유형 | 레거시 로직 제거 → 진입점 위임 |
| Before | 37줄 단일 `main()` (입력·검증·변환·출력 혼재) |
| After | 4줄 — `from src.cli import main` |
| 목적 | README 실행 경로(`python UnitConverter.py`) 유지 + SRP 분리 |

**제거된 레거시 책임 (→ `src/`로 이전)**

| 레거시 줄 | 책임 | 이전 대상 |
|-----------|------|-----------|
| L2 | `input()` 프롬프트 | `src/cli.py` — `main()` |
| L4–6 | `:` 형식 검사 | `src/cli.py` — `run()` |
| L8–14 | split + `float` | `src/parser.py` — `parse_input()` |
| L16–24 | 단위 if/elif | `src/registry.py` + `src/cli.py` |
| L26–28 | meter 허브 변환 | `src/converter.py` — `convert()` |
| L30–32 | `print` 출력 | `src/cli.py` — `run()` |

#### `tests/Boundary/test_cli.py`

| 항목 | 내용 |
|------|------|
| 변경 유형 | FR-01 GREEN 검증 강화 + import 경로 정리 |
| 주요 변경 | `@pytest.mark.track("UI")` 추가 |
| | `ParsedInput` 타입 검증 (`isinstance`) 추가 |
| | 주석 import `boundary.*` → `src.*` 로 통일 (FR-06~12 RED 스텁) |

---

### 3.2 신규 (Untracked) — `src/` 패키지

| 파일 | Layer | 역할 | FR/NFR |
|------|-------|------|--------|
| `src/__init__.py` | — | 패키지 선언 | — |
| `src/constants.py` | entity | 변환 상수 SSOT (`3.28084`, `1.09361`) | NFR-01 |
| `src/parsed_input.py` | boundary | `ParsedInput` DTO | FR-01 |
| `src/parser.py` | boundary | `parse_input()` — split·trim·float | FR-01, FR-11(로직 선행) |
| `src/conversion_result.py` | entity | `ConversionResult` DTO | FR-02 |
| `src/registry.py` | entity | `UnitRegistry` — 단위·비율·meter 허브 | NFR-01, FR-04 |
| `src/converter.py` | domain/control | `Converter.convert()` — 소스 단위 제외 변환 | FR-02, FR-04 |
| `src/cli.py` | boundary | `run()`, `main()` — I/O·오케스트레이션 | NFR-03, NFR-08 |

**의존 방향 (`src/` 내부)**

```
cli.py ──→ parser.py, registry.py, converter.py
parser.py ──→ parsed_input.py
converter.py ──→ conversion_result.py, registry.py
registry.py ──→ constants.py
```

---

### 3.3 신규 (Untracked) — `entity/` 패키지 (초안)

| 파일 | 상태 |
|------|------|
| `entity/__init__.py` | ECB entity 레이어 초안 |
| `entity/constants.py` | `src/constants.py`와 동일 SSOT |
| `entity/conversion_result.py` | `src/conversion_result.py`와 동일 DTO |
| `entity/registry.py` | `src/registry.py`와 유사 구현 |

> **주의:** `entity/`는 **테스트·`src/cli`와 연동되지 않음**. ECB 분리 예비 작업으로 보이며, 실제 GREEN 구현은 현재 **`src/` 패키지**에 위치한다. 커밋 시 `src/`와 중복 여부 검토 필요.

---

### 3.4 기타 Untracked (Report 제외 대상)

| 경로 | 비고 |
|------|------|
| `boundary/__pycache__/` | 이전 `boundary/*.py` 삭제 후 잔존 캐시 |
| `tests/**/__pycache__/` | pytest 실행 캐시 — `.gitignore` 권장 |

---

## 4. 아키텍처 As-Is → To-Be

### 4.1 Before (커밋 `0dc5ecb` 기준)

```
UnitConverter.py          # 37줄 God Function
tests/Boundary/           # RED TC (pytest.fail)
tests/Domain/             # RED TC (pytest.fail)
```

### 4.2 After (현재 working tree)

```
UnitConverter.py          # 진입점 (4줄)
src/
  constants.py            # SSOT
  parsed_input.py         # Boundary DTO
  parser.py               # Boundary — 파싱
  conversion_result.py    # Entity DTO
  registry.py             # Entity — Registry
  converter.py            # Domain — 변환
  cli.py                  # Boundary — CLI
tests/
  Boundary/test_cli.py    # FR-01 GREEN
  Domain/test_converter.py # FR-02 GREEN
entity/                   # (미연동 초안)
```

---

## 5. 레거시 → 모듈 분리 매핑표

| 레거시 스멜 | 해소 방향 | 현재 상태 |
|-------------|-----------|-----------|
| God Function / SRP 위반 | `parser`, `registry`, `converter`, `cli` 분리 | ✅ 부분 해소 |
| Magic Number 반복 | `src/constants.py` SSOT | ✅ 해소 |
| OCP 위반 (if/elif) | `UnitRegistry` + `Converter` | ✅ 부분 해소 |
| I/O와 도메인 혼재 | `cli.run()` / `parse_input()` 분리 | ✅ 부분 해소 |
| 테스트 불가 | pytest FR-01/02 통과 | ✅ 부분 해소 |

**아직 미해소 (다음 GREEN 대상)**

| FR | 내용 | 현재 |
|----|------|------|
| FR-03 | 소수 1자리 반올림 | 미구현 (`formatter` 없음) |
| FR-05 | 단수형 표기 검증 | Converter는 단수형 사용, TC RED |
| FR-06~12 | validator 분리 | `src/validator.py` 없음, TC RED |
| FR-08 | 음수 거부 | cli/parser 미검증 |
| FR-10 | 빈 unit/value | cli/parser 미검증 |

---

## 6. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

| # | Test ID | Req | Track | 결과 |
|---|---------|-----|-------|------|
| 1 | TC-FR-01 | FR-01 | UI | **PASS** |
| 2 | TC-FR-02 | FR-02 | Logic | **PASS** |
| 3 | U-FR-06 ~ U-FR-12 | FR-06~12 | UI | FAIL (RED) |
| 4 | D-FR-03 ~ D-FR-05 | FR-03~05 | Logic | FAIL (RED) |

**합계:** 13 collected — **2 passed, 11 failed**

### 6.1 개별 TC 실행 명령

```bash
# GREEN 통과 TC
python -m pytest tests/Boundary/test_cli.py::test_tc_fr_01_parse_meter_2_5 -v
python -m pytest tests/Domain/test_converter.py::test_tc_fr_02_convert_all_units_excluding_source -v

# 전체
python -m pytest tests/ -v
```

---

## 7. CLI 동작 확인 (수동)

```bash
python UnitConverter.py
# 또는
python -c "from src.cli import run; run('meter:2.5')"
```

**예상 출력 (FR-03 반올림 미적용 — raw float):**

```
2.5 meter = 8.2021 feet
2.5 meter = 2.734025 yard
```

> PRD/README 예시(`8.2 feet`, `2.7 yard`)와 차이 — FR-03 `formatter` GREEN 후 일치 예정.

---

## 8. 커밋 권장 사항

### 8.1 포함 권장

- `UnitConverter.py`
- `src/**` (`.py`만)
- `tests/Boundary/test_cli.py`

### 8.2 제외 권장

- `**/__pycache__/`
- `boundary/` (소스 없음, 캐시만)
- `entity/` — `src/`와 중복·미연동 시 정리 후 별도 커밋

### 8.3 제안 커밋 메시지 (참고)

```
레거시 UnitConverter.py를 src 패키지로 분리하고 FR-01/FR-02 GREEN을 구현합니다.
```

---

## 9. 다음 단계

| 순서 | 작업 | 대상 FR |
|------|------|---------|
| 1 | `src/validator.py` 추가 + TC GREEN | FR-06~12 |
| 2 | `src/formatter.py` 추가 + TC GREEN | FR-03, FR-05 |
| 3 | `entity/` vs `src/` ECB 정렬 또는 `entity/` 제거 | NFR-02 |
| 4 | `.gitignore`에 `__pycache__/` 추가 | — |
| 5 | GREEN 브랜치 커밋·push | — |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| PRD Report | [Report/01_unit-converter-prd-report.md](./01_unit-converter-prd-report.md) |
| Cursor Rules | [.cursor/rules/.cursorrules](../.cursor/rules/.cursorrules) |
| 레거시 (변경 후) | [UnitConverter.py](../UnitConverter.py) |
| 구현 패키지 | [src/](../src/) |
