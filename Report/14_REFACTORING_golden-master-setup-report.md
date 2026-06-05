# 14 — REFACTORING Golden Master 설정 Report

| 항목 | 내용 |
|------|------|
| Report ID | 14 (REFACTORING) |
| 작성일 | 2026-06-05 |
| 기준 브랜치 | `REFACTORING` (로컬, `GREEN` `97da13d`에서 분기) |
| 기준 커밋 | `97da13d` — P0 FR 12/12 GREEN (PR7 완료) |
| 대상 | `git status` 기준 **미커밋(uncommitted)** 변경분 |
| Phase | REFACTORING — Golden Master 무결성 확보 (1차) |
| 상태 | Draft — 커밋 전 |

---

## 1. Report 목적

본 Report는 **REFACTORING 단계 Golden Master** 도입의 `git status` 변경분을 기록한다.

- `cli.run()` stdout 스냅샷(9케이스) 생성·비교 TC 추가 내역을 문서화한다.
- P0 FR TC(13건)와 Golden Master TC(9건) **이중 안전망** 구조를 정리한다.
- `README.md` REFACTORING·Golden Master 실행 방법 갱신을 기록한다.
- 후속 리팩토링(`cli`↔`validator` 연동 등) 진입점을 제공한다.

---

## 2. Git Status 스냅샷

```
On branch REFACTORING

Changes not staged for commit:
  modified:   src/__pycache__/*.pyc              (커밋 제외 권장)

Untracked files:
  golden_master/
  scripts/generate_golden_master.py
  tests/GoldenMaster/
  Report/14_REFACTORING_golden-master-setup-report.md
  README.md                                    (갱신 — 미스테이징 시 working tree)
  boundary/                                  (__pycache__ 잔존만)
  tests/**/__pycache__/
```

### 2.1 신규 파일 목록

| 구분 | 경로 | 역할 |
|------|------|------|
| **신규** | `golden_master/cases.json` | 9개 입력 케이스 정의 |
| **신규** | `golden_master/expected/*.txt` | 기준 stdout (9 files) |
| **신규** | `scripts/generate_golden_master.py` | expected 재생성 스크립트 |
| **신규** | `tests/GoldenMaster/test_golden_master.py` | parametrize 회귀 TC |
| **수정** | `README.md` | REFACTORING·Golden Master ToDo |

> **`src/` 로직 변경 없음** — 리팩토링 전 동작 고정용 인프라만 추가.

---

## 3. Golden Master 설계

### 3.1 대상 API

| API | Layer | Golden Master |
|-----|-------|:-------------:|
| `cli.run(input_str)` | Boundary I/O | **✅ 스냅샷 대상** |
| `validate_input()` | Boundary | FR TC로 검증 (13건) |
| `parse_input()` / `Converter` | Boundary/Domain | FR TC로 검증 |

**이유:** Golden Master는 **사용자 가시 출력(end-to-end boundary)** 을 고정한다. `validator`는 아직 `cli.run()`에 미연동.

### 3.2 케이스 (`golden_master/cases.json`)

| id | input | 스냅샷 요약 |
|----|-------|-------------|
| `meter_2_5` | `meter:2.5` | 정상 변환 2줄 (raw float) |
| `meter_no_colon` | `meter` | 형식 오류 |
| `meter_abc` | `meter:abc` | 숫자 오류 |
| `meter_negative` | `meter:-1` | **음수 변환** (validator 미연동) |
| `cubit_1` | `cubit:1` | Unknown unit |
| `empty_unit` | `:2.5` | Unknown unit (cli 현재 동작) |
| `empty_value` | `meter:` | Invalid number |
| `whitespace_trim` | ` meter : 2.5 ` | trim 후 변환 |
| `case_sensitive` | `Meter:2.5` | Unknown unit (대소문자) |

> `validator`와 `cli.run()` 차이(예: `":2.5"`, `meter:-1`)는 **의도적으로 cli 기준** 고정.

### 3.3 기준 파일 위치

```
golden_master/expected/   ← Approve(기준) stdout — "Approve" 폴더명은 사용하지 않음
```

---

## 4. 실행 방법

### 4.1 Golden Master 생성/재생성

```bash
python scripts/generate_golden_master.py
```

### 4.2 Golden Master TC

```bash
python -m pytest tests/GoldenMaster/test_golden_master.py -v
# 9 passed
```

### 4.3 전체 (FR + Golden Master)

```bash
python -m pytest tests/ -v
# 22 passed
```

---

## 5. TC 실행 결과 (Report 작성 시점)

| Track | 파일 | PASS |
|-------|------|------|
| Boundary FR | `tests/Boundary/test_cli.py` | 9 |
| Domain FR | `tests/Domain/test_converter.py` | 4 |
| **Golden Master** | `tests/GoldenMaster/test_golden_master.py` | **9** |
| **합계** | | **22** |

> P0 FR 13건 회귀 없음 + Golden Master 9건 추가.

---

## 6. REFACTORING 워크플로

```
97da13d (GREEN) ──→ REFACTORING 브랜치 생성
       │
       ├─ Golden Master 스냅샷 커밋          ← 본 Report
       ├─ 리팩토링 (cli↔validator, formatter 연동 등)
       ├─ pytest tests/ — golden master diff 확인
       └─ 의도적 변경 시 generate_golden_master.py 재실행
```

---

## 7. 커밋 권장 사항

### 7.1 포함 권장

```
golden_master/cases.json
golden_master/expected/*.txt
scripts/generate_golden_master.py
tests/GoldenMaster/test_golden_master.py
README.md
Report/14_REFACTORING_golden-master-setup-report.md
```

### 7.2 제외 권장

- `**/__pycache__/**`
- `boundary/` (pycache 잔존만)
- `Report/*-transcript.md` (선택)

### 7.3 제안 커밋 메시지

```
Golden Master 스냅샷과 회귀 TC를 추가하여 REFACTORING 무결성 기반을 마련합니다.
```

### 7.4 REFACTORING (1차) 제안 제목

```
REFACTORING: Golden Master setup (cli.run snapshot + 9 regression tests)
```

---

## 8. 다음 단계

| 순서 | 작업 | 비고 |
|------|------|------|
| 1 | 본 변경분 커밋 + `REFACTORING` push | Golden Master baseline |
| 2 | `cli.run()` → `validate_input()` 연동 | golden diff 예상 |
| 3 | `formatter` 출력 형식 연동 | golden/FR TC 정렬 |
| 4 | 의도적 변경 시 expected 재생성 | `generate_golden_master.py` |
| 5 | Report 15 — cli-validator 연동 | REFACTORING 2차 |

---

## 9. 관련 문서

| 문서 | 경로 |
|------|------|
| README ToDo | [README.md](../README.md) |
| Report 13 (PR7 완료) | [Report/13_PR7_fr12-case-sensitive-unit-green-report.md](./13_PR7_fr12-case-sensitive-unit-green-report.md) |
| Golden cases | [golden_master/cases.json](../golden_master/cases.json) |
| Generate script | [scripts/generate_golden_master.py](../scripts/generate_golden_master.py) |
| Golden TC | [tests/GoldenMaster/test_golden_master.py](../tests/GoldenMaster/test_golden_master.py) |
| CLI | [src/cli.py](../src/cli.py) |
