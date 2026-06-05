# 06 — PR5 Domain FR-03~05 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 06 (PR5) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `dec4604` — README ToDo + PR3 Report |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Domain Track FR-03, FR-04, FR-05 |
| PR | PR5 — Domain P0 FR **전체 GREEN** |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Domain Track FR-03~FR-05 GREEN** 작업의 `git status` 변경분을 기록한다.

- `src/formatter.py` 신규 추가 (FR-03 반올림) 내역을 문서화한다.
- FR-04·FR-05 TC 활성화(기존 `Converter`/`Registry` 활용) 범위를 명확히 한다.
- **Domain P0 FR 4건(FR-02~05) GREEN 완료** 스냅샷을 PR5 리뷰 자료로 제공한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   tests/Domain/test_converter.py
  modified:   src/__pycache__/*.pyc          (커밋 제외 권장)

Untracked files:
  src/formatter.py                           (신규 — FR-03)
  Report/05_PR4_fr04-derived-conversion-report.md
  Report/05_PR4_fr04-derived-conversion-report-transcript.md
  boundary/              (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 Diff 통계

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| 신규 | `src/formatter.py` | +18 | — |
| 수정 | `tests/Domain/test_converter.py` | +34 | −42 |
| 제외 | `src/__pycache__/*.pyc` | — | — |

---

## 3. 변경 파일 상세

### 3.1 신규 — `src/formatter.py` (FR-03)

| 함수 | 역할 | FR |
|------|------|-----|
| `round_half_up(value, decimals=1)` | `Decimal` + `ROUND_HALF_UP` | FR-03 |
| `format_conversions(source_unit, value)` | Converter → `"8.2 feet"` 형식 목록 | FR-03 |

**변환 예 (`meter:2.5`)**

| 단위 | raw value | round half up (1자리) | 출력 |
|------|-----------|----------------------|------|
| feet | 8.2021 | 8.2 | `"8.2 feet"` |
| yard | 2.734025 | 2.7 | `"2.7 yard"` |

**의존:** `Converter`, `UnitRegistry.default()` — 기존 PR1 구현 재사용.

### 3.2 수정 — `tests/Domain/test_converter.py`

| Test ID | Req | 변경 | src 변경 |
|---------|-----|------|----------|
| D-FR-03 | FR-03 | `format_conversions` GREEN | **`src/formatter.py` 신규** |
| D-FR-04 | FR-04 | `Converter.convert` GREEN, SSOT 기대값 | 없음 |
| D-FR-05 | FR-05 | `output_units` 단수형 검증 GREEN | 없음 |

#### D-FR-03 (FR-03)

```python
from src.formatter import format_conversions
lines = format_conversions("meter", 2.5)
# assert "8.2 feet", "2.7 yard"
```

#### D-FR-04 (FR-04)

- 입력: `feet:FEET_PER_METER` (≡ 1 meter)
- 기대: `yard ≈ YARD_PER_METER` (`1.09361`)
- PRD Then `yard ≈ 1.0` → SSOT 상수로 정렬 (Report 05 참조)

#### D-FR-05 (FR-05)

- `output_units == {"feet", "yard"}`
- 복수형 `feets`, `yards`, `meters` 미포함

---

## 4. 아키텍처 — PR5 이후 Domain 흐름

```
src/formatter.py  ──→ src/converter.py ──→ src/entity/registry.py
       │                      │
   FR-03 반올림            FR-02/04/05 변환
   "8.2 feet"              ConversionResult
```

| Layer | 모듈 | FR | PR |
|-------|------|-----|-----|
| Domain | `src/converter.py` | FR-02, FR-04, FR-05 | PR1 |
| Domain | **`src/formatter.py`** | **FR-03** | **PR5** |
| Entity | `src/entity/*` | SSOT, Registry | PR1·PR3 |

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Domain — `tests/Domain/test_converter.py`

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-02 | FR-02 | **PASS** |
| D-FR-03 | FR-03 | **PASS** ← PR5 (formatter) |
| D-FR-04 | FR-04 | **PASS** ← PR5 |
| D-FR-05 | FR-05 | **PASS** ← PR5 |

```bash
python -m pytest tests/Domain/test_converter.py -v
# 4 passed
```

### 5.2 전체

| Track | PASS | FAIL |
|-------|------|------|
| Domain (4) | **4** | 0 |
| Boundary (9) | 1 (FR-01) | 8 (RED) |
| **합계 (13)** | **5** | **8** |

---

## 6. README ToDo 대비 진행 (PR5 반영)

### P0 FR — Domain (Track B)

| Req ID | RED | GREEN (PR5 전) | GREEN (PR5 후) |
|--------|:---:|:--------------:|:--------------:|
| FR-02 | ✅ | ✅ PR1 | ✅ |
| FR-03 | ✅ | ⬜ | **✅ PR5** |
| FR-04 | ✅ | ⬜ | **✅ PR5** |
| FR-05 | ✅ | ⬜ | **✅ PR5** |

**Domain P0 FR:** **4/4 GREEN 완료**

### P0 FR — Boundary (Track A) — 미변경

| Req ID | GREEN |
|--------|:-----:|
| FR-01 | ✅ PR1 |
| FR-06~12 | ⬜ PR6 예정 |

**P0 FR 전체 GREEN:** 5/12 (FR-01, FR-02~05)

---

## 7. PR5 vs PR4 비교

| PR | 범위 | src 신규 | Domain GREEN |
|----|------|----------|--------------|
| PR4 | FR-04 TC만 | — | FR-02, FR-04 |
| **PR5** | FR-03~05 | **`formatter.py`** | **FR-02~05 전체** |

---

## 8. 커밋 권장 사항 (PR5)

### 8.1 포함 권장

```
src/formatter.py
tests/Domain/test_converter.py
Report/05_PR4_fr04-derived-conversion-report.md        (미커밋 시)
Report/05_PR4_fr04-derived-conversion-report-transcript.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/`

### 8.3 제안 커밋 메시지

```
FR-03 Formatter 추가 및 Domain FR-03~05 GREEN을 완료합니다.
```

### 8.4 PR5 제안 제목

```
PR5: Domain FR-03~05 GREEN (formatter + derived conversion + unit names)
```

---

## 9. 다음 단계 (PR6)

| 순서 | 작업 | FR |
|------|------|-----|
| 1 | `src/validator.py` 구현 | FR-06~12 |
| 2 | FR-11 TC 활성화 (parse_input strip 이미 구현) | FR-11 |
| 3 | `cli.py` → `formatter` 연동 (README 출력 형식) | FR-03 |
| 4 | README ToDo GREEN 컬럼 갱신 | — |
| 5 | NFR P0 TC 작성·GREEN | NFR-01~08 |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 05 (PR4) | [Report/05_PR4_fr04-derived-conversion-report.md](./05_PR4_fr04-derived-conversion-report.md) |
| Formatter | [src/formatter.py](../src/formatter.py) |
| Domain TC | [tests/Domain/test_converter.py](../tests/Domain/test_converter.py) |
