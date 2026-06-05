# 12 — PR7 Boundary FR-11 GREEN 변경 Report

| 항목 | 내용 |
|------|------|
| Report ID | 12 (PR7) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `GREEN` (`origin/GREEN` 추적) |
| 기준 커밋 | `7ce6da6` — FR-10 빈 unit/value + TC-FR-10 GREEN (PR7 5차) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | GREEN — Boundary Track FR-11 (공백 trim) |
| PR | PR7 — U-FR-11 / TC-FR-11 GREEN (6차) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **Boundary Track FR-11 GREEN** 작업의 `git status` 변경분을 기록한다.

- FR-11 TC 활성화(기존 `parse_input` strip 활용) 범위를 문서화한다.
- **`src/` 코드 변경 없음** — PR1 `parser.py` 구현으로 GREEN 처리한 최소 범위를 명확히 한다.
- `README.md` ToDo 갱신(FR-11·11/12 GREEN)을 정리한다.
- FR-12 RED 유지 및 PR7 마무리 진입점을 제공한다.

---

## 2. Git Status 스냅샷

```
On branch GREEN
Your branch is up to date with 'origin/GREEN'.

Changes not staged for commit:
  modified:   README.md
  modified:   src/__pycache__/*.pyc              (커밋 제외 권장)
  modified:   tests/Boundary/test_cli.py

Untracked files:
  Report/12_PR7_fr11-whitespace-trim-green-report.md
  boundary/                                  (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 Diff 통계 (소스·테스트·문서)

| 구분 | 파일 | 삽입 | 삭제 |
|------|------|------|------|
| **수정** | `tests/Boundary/test_cli.py` | +5 | −9 |
| **수정** | `README.md` | (FR-11·11/12 반영) | — |
| **`src/` 소스** | — | **0** | **0** |
| 제외 | `src/__pycache__/*.pyc` | — | — |

> **핵심:** FR-11는 **테스트 파일 1건만** 변경. `parse_input` strip은 PR1에서 이미 구현됨.

---

## 3. 변경 파일 상세

### 3.1 변경 없음 — `src/parser.py` (FR-11 구현 SSOT)

PR1 GREEN 시 이미 strip 적용:

```python
def parse_input(input_str: str) -> ParsedInput:
    unit, value_str = input_str.split(":", 1)
    return ParsedInput(
        unit=unit.strip(),
        value=float(value_str.strip()),
    )
```

| Given | Then |
|-------|------|
| `" meter : 2.5 "` | `unit="meter"`, `value=2.5` |

**설계 메모**

- FR-11은 **파싱(trim)** 책임 → `validator`가 아닌 **`parser`**.
- `validator.py`도 `unit_str.strip()` 사용 — FR-10·09와 정합.

### 3.2 수정 — `tests/Boundary/test_cli.py` (U-FR-11 GREEN)

| 항목 | Before (RED) | After (GREEN) |
|------|--------------|---------------|
| 상태 | `pytest.fail("RED: FR-11 ...")` | `parse_input()` + assert |
| import | 주석 처리 | `from src.parser import parse_input` |
| assert | 주석 | `unit == "meter"`, `value == 2.5` |

```python
result = parse_input(" meter : 2.5 ")
assert result.unit == "meter"
assert result.value == 2.5
```

### 3.3 수정 — `README.md` (ToDo 갱신)

| 섹션 | 변경 요약 |
|------|----------------|
| 헤더 | PR7 (FR-06~**11** GREEN) |
| 전체 GREEN | 10/12 → **11/12** |
| PR7 마일스톤 | `7ce6da6` — FR-06~**11**, FR-12 잔여 |
| Boundary FR-11 | GREEN ✅ |
| `src/parser.py` | FR-01, **FR-11** ✅ |
| TC 결과 | **12 passed**, 1 failed |

---

## 4. 아키텍처 — FR-11 역할 분리

```
tests/Boundary/test_cli.py
    │
    ├─ FR-01, FR-11  →  src/parser.py       parse_input() + strip
    └─ FR-06~10      →  src/validator.py    validate_input()
```

| Layer | 모듈 | FR | 변경 |
|-------|------|-----|------|
| Boundary | `src/parser.py` | FR-01, **FR-11** | **없음 (PR1)** |
| Boundary | `tests/Boundary/test_cli.py` | FR-11 | **TC 활성화** |

---

## 5. TC 실행 결과 (Report 작성 시점)

**명령:** `python -m pytest tests/ -v`

### 5.1 Boundary — FR-11 단건

```bash
python -m pytest tests/Boundary/test_cli.py::test_u_fr11_whitespace_trim -v
# 1 passed
```

### 5.2 Boundary — `tests/Boundary/test_cli.py` 전체

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-01 | FR-01 | **PASS** |
| U-FR-06 ~ U-FR-11 | FR-06~11 | **PASS** |
| U-FR-12 | FR-12 | FAIL (RED) |

```bash
python -m pytest tests/Boundary/test_cli.py -v
# 8 passed, 1 failed
```

### 5.3 Domain — 회귀 없음

| Test ID | Req | 결과 |
|---------|-----|------|
| TC-FR-02 ~ D-FR-05 | FR-02~05 | **PASS** (4건) |

### 5.4 전체 합계

| Track | PASS | FAIL |
|-------|------|------|
| Boundary (9) | **8** | 1 (RED) |
| Domain (4) | **4** | 0 |
| **합계 (13)** | **12** | **1** |

> Report 11 대비: **+1 PASS** (FR-11). FR-06~10·FR-01 회귀 없음.

---

## 6. README ToDo 대비 진행 (FR-11 반영)

### P0 FR — Boundary (Track A)

| Req ID | GREEN (Report 11) | GREEN (Report 12) |
|--------|:-----------------:|:-----------------:|
| FR-06~10 | ✅ | ✅ |
| **FR-11** | ⬜ | **✅ PR7 6차** |
| FR-12 | ⬜ | ⬜ |

### P0 FR 전체

| 시점 | GREEN |
|------|:-----:|
| Report 11 (FR-10) | 10/12 |
| **Report 12 (FR-11)** | **11/12** |

---

## 7. PR7 진행 비교 (5차 vs 6차)

| 차수 | 커밋 | FR | `src/` 변경 |
|------|------|-----|-------------|
| 5차 | `7ce6da6` | FR-10 빈 unit/value | `validator.py` |
| **6차** | (미커밋) | **FR-11 trim** | **없음 (TC만)** |

---

## 8. 커밋 권장 사항 (PR7 FR-11)

### 8.1 포함 권장

```
tests/Boundary/test_cli.py
README.md
Report/12_PR7_fr11-whitespace-trim-green-report.md
```

### 8.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)

### 8.3 제안 커밋 메시지

```
FR-11 공백 trim TC-FR-11 GREEN을 활성화하고 README ToDo를 갱신합니다.
```

### 8.4 PR7 (6차) 제안 제목

```
PR7: Boundary FR-11 GREEN (parser whitespace trim — TC only)
```

---

## 9. 다음 단계 (PR7 마무리)

| 순서 | 작업 | FR |
|------|------|-----|
| 1 | 대소문자 거부 | FR-12 (`Meter` → Unknown unit) |
| 2 | `cli.py` → `validator` 연동 | FR-06~12 |
| 3 | README ToDo FR-12 GREEN · P0 FR 12/12 | — |
| 4 | NFR P0 TC (PR8) | NFR-01~08 |

---

## 10. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README ToDo | [README.md](../README.md) |
| Report 11 (PR7 5차) | [Report/11_PR7_fr10-empty-unit-value-green-report.md](./11_PR7_fr10-empty-unit-value-green-report.md) |
| Parser | [src/parser.py](../src/parser.py) |
| Boundary TC | [tests/Boundary/test_cli.py](../tests/Boundary/test_cli.py) |
