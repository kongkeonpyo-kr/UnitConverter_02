# Unit Converter — Product Requirements Document (PRD)

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.2 |
| 작성일 | 2026-06-05 |
| 기준 문서 | [README.md](../README.md) |
| 레거시 코드 | [UnitConverter.py](../UnitConverter.py) |
| 상태 | Draft |

---

## 1. 개요

### 1.1 목적

사용자가 입력한 길이(`단위:값`)를 기반으로 해당 값을 다른 모든 단위로 변환해 출력하는 Python CLI 프로그램을, 확장 가능하고 테스트 가능한 구조로 재설계·구현한다.

### 1.2 배경

현재 `UnitConverter.py`는 37줄 단일 스크립트로 핵심 변환 기능만 동작한다. README에 정의된 품질 요구(OCP, SRP, 입력 검증, 테스트)와 추가 요구(설정 외부화, 동적 단위 등록, 출력 포맷)는 미구현 상태이다.

### 1.3 As-Is → To-Be

| 구분 | As-Is (레거시) | To-Be (목표) |
|------|----------------|--------------|
| 구조 | 단일 `main()` 함수 | SRP/OCP를 만족하는 클래스·모듈 분리 |
| 비율 | 하드코딩 Magic Number | 외부 설정 + 기준 단위(meter) 단일 정의 |
| 단위 확장 | if/elif 분기 수정 필요 | 레지스트리/인터페이스 기반 확장 |
| 검증 | 형식·숫자·미지 단위만 | 음수·엣지 케이스 포함 전체 검증 |
| 출력 | 고정 텍스트 `print` | JSON / CSV / 표 형태 선택 |
| 테스트 | 없음 | 단위 변환·입력 검증 TC |
| 설정 | 없음 | JSON/YAML 외부 설정 + 동적 등록 |

---

## 2. 사용자 및 사용 시나리오

### 2.1 대상 사용자

- 길이 단위를 빠르게 변환해야 하는 CLI 사용자
- 실습 참가자(생성형 AI 활용 리팩토링 Activities, 6시간)

### 2.2 핵심 사용자 스토리

| ID | 스토리 | 우선순위 |
|----|--------|----------|
| US-01 | 사용자로서 `meter:2.5` 형식으로 입력하면 모든 지원 단위로 변환 결과를 볼 수 있다 | P0 |
| US-02 | 사용자로서 잘못된 입력(형식, 숫자, 음수, 미지 단위) 시 명확한 오류 메시지를 받는다 | P0 |
| US-03 | 개발자로서 새 단위 추가 시 기존 변환 로직을 수정하지 않고 등록만으로 확장할 수 있다 | P0 |
| US-04 | 사용자로서 변환 비율을 JSON/YAML 설정 파일에서 로드할 수 있다 | P1 |
| US-05 | 사용자로서 `1 cubit = 0.4572 meter`처럼 런타임에 단위를 등록해 사용할 수 있다 | P1 |
| US-06 | 사용자로서 변환 결과를 JSON, CSV, 표 형태 중 하나로 출력할 수 있다 | P1 |

---

## 3. 기능 요구사항

### 3.1 FR Track 개요 — Domain vs Boundary

FR(기능 요구)은 **헥사고날 / 클린 아키텍처** 관점에서 두 Track으로 구분한다.

| Track | 명칭 | 범위 | 대표 모듈 | Test File |
|-------|------|------|-----------|-----------|
| **Track B** | **Domain** | 단위 변환·반올림·표기 등 **핵심 비즈니스 규칙** | `converter.py`, `formatter.py`, `registry.py` | `tests/test_converter.py` |
| **Track A** | **Boundary** | CLI 입출력·입력 파싱·검증·오류 응답 등 **시스템 경계** | `cli.py`, `parser.py`, `validator.py` | `tests/test_cli.py` |

```
[Track A: Boundary]          [Track B: Domain]
  test_cli.py                   test_converter.py
       │                              │
  FR-01 파싱 ──────────────────► FR-02 변환
  FR-06~12 검증                    FR-03 반올림
       │                           FR-04 파생 변환
  CLI 입출력·exit code              FR-05 단위 표기
```

**공통 입력 형식:** `{unit}:{value}` (예: `meter:2.5`)

**초기 지원 단위:**

| 단위 | 기준(meter) 대비 비율 |
|------|----------------------|
| meter | 1 (기준) |
| feet | 1 meter = 3.28084 feet |
| yard | 1 meter = 1.09361 yard |

**비즈니스 규칙 (Domain):**

- feet/yard 간 비율은 meter를 기준으로 파생 계산한다.
- 변환 비율은 단일 소스(기준 단위 + 설정)에서 관리한다.

**출력 예시 (표 형태, 소수 1자리 반올림):**

```
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

### 3.2 Track B — Domain (P0) — FR-02 ~ FR-05

> **Test File:** `tests/test_converter.py`

변환 엔진 내부에서 I/O 없이 검증 가능한 **도메인 규칙**.

| ID | Track | 요구 | 설명 |
|----|-------|------|------|
| FR-02 | B | 전 단위 변환 출력 | 등록된 모든 단위로 변환 (소스 단위 제외) |
| FR-03 | B | 소수 1자리 반올림 | round half up, 예: 8.2 feet, 2.7 yard |
| FR-04 | B | meter 기준 파생 변환 | feet↔yard 등 비 meter 단위 간 변환도 meter 경유 |
| FR-05 | B | 단위 표기 | 단수형 `meter`, `feet`, `yard` |

- 소수점 표시: **소수 1자리**, 반올림(round half up)
- **입력(소스) 단위는 출력에서 제외** — 다른 모든 단위만 표시
- 단위 표기: README 예시와 동일하게 단수형 (`meter`, `feet`, `yard`)

### 3.3 Track A — Boundary (P0) — FR-01, FR-06 ~ FR-12

> **Test File:** `tests/test_cli.py`

CLI 경계에서 수신·거부·전달되는 **입력 처리 및 검증**.

| ID | Track | 검증 항목 | 조건 | 오류 메시지 (예시) |
|----|-------|-----------|------|-------------------|
| FR-01 | A | 입력 파싱 | `unit:value` 문자열을 unit, value로 분리 | — |
| FR-06 | A | 형식 | `:` 구분자 필수 | `Invalid format. Use unit:value (ex: meter:2.5)` |
| FR-07 | A | 숫자 | value는 float 변환 가능 | `Invalid number: {value_str}` |
| FR-08 | A | 음수 | value < 0 거부 | `Negative values are not allowed: {value}` |
| FR-09 | A | 단위 | 등록된 단위만 허용 | `Unknown unit: {unit}` |
| FR-10 | A | 빈 값 | unit 또는 value가 빈 문자열 | `Invalid format. Unit and value must not be empty` |
| FR-11 | A | 공백 | unit/value 앞뒤 trim 후 처리 | — |
| FR-12 | A | 대소문자 | 단위명은 **소문자만** 허용 (초기 MVP) | `Unknown unit: {unit}` |

### 3.4 아키텍처 요구 (P0) — NFR-01 ~ NFR-03

README 품질 요구를 PRD 수준으로 구체화한다.

| ID | 원칙 | 요구사항 |
|----|------|----------|
| NFR-01 | **OCP** | 단위 추가 시 기존 Converter/Formatter 코드 수정 없이 Registry 확장만으로 가능 |
| NFR-02 | **SRP** | Parser, Validator, Converter, Formatter, UnitRegistry 등 역할별 클래스 분리 |
| NFR-03 | **테스트 가능성** | I/O(`input`/`print`)와 도메인 로직 분리, pytest로 단위 테스트 가능 |

**권장 모듈 구조 (참고):**

```
src/
  parser.py          # Track A — 입력 파싱
  validator.py       # Track A — 입력 검증
  cli.py             # Track A — CLI 진입점
  registry.py        # Domain — 단위 등록·조회
  converter.py       # Track B — 변환 로직
  formatter.py       # Track B — 출력 포맷 (text/json/csv)
  config_loader.py   # 설정 파일 로드
tests/
  test_cli.py        # Track A — Boundary FR (FR-01, FR-06~12)
  test_converter.py  # Track B — Domain FR (FR-02~05)
  ...
config/
  units.json         # 기본 단위 비율
```

### 3.5 설정 외부화 (P1) — EXT-01 ~ EXT-04

| ID | 요구 | 설명 |
|----|------|------|
| EXT-01 | 설정 파일 로드 | `config/units.json`에서 비율 로드 |
| EXT-02 | 설정 누락 기본값 | 파일 없을 때 내장 기본 비율 사용 |
| EXT-03 | 설정 파싱 실패 | malformed JSON/YAML 시 오류 + exit 1 |
| EXT-04 | `--config` 옵션 | 사용자 지정 설정 파일 경로 지원 |

- 변환 비율을 **JSON 또는 YAML** 외부 파일에서 로드한다.
- 기본 설정 파일: `config/units.json`
- CLI 옵션: `--config <path>` (선택)
- 설정 파일 스키마 (JSON 예시):

```json
{
  "base_unit": "meter",
  "units": {
    "meter": 1,
    "feet": 3.28084,
    "yard": 1.09361
  }
}
```

- `units` 값: **1 base_unit = N {unit}** 형식
- 설정 파일 누락 시: 내장 기본값 사용
- 설정 파일 파싱 실패 시: 오류 메시지 출력 후 종료 (exit code 1)

### 3.6 동적 단위 등록 (P1) — EXT-05 ~ EXT-06

| ID | 요구 | 설명 |
|----|------|------|
| EXT-05 | 동적 단위 등록 | `--register "cubit:0.4572"` 등으로 Registry에 추가 |
| EXT-06 | 등록 후 즉시 변환 | 등록 직후 변환 대상 단위 목록에 포함 |

- 사용자가 런타임에 새 단위를 등록할 수 있다.
- 등록 문법: `{new_unit} = {ratio} {base_unit}` (예: `1 cubit = 0.4572 meter`)
- 등록 방법 (MVP): CLI 대화형 프롬프트 또는 `--register "cubit:0.4572"` 인자
- 등록된 단위는 **현재 세션(프로세스) 동안만** 유효 (영속 저장은 Phase 2)
- 등록 후 즉시 변환 대상 단위 목록에 포함

### 3.7 출력 포맷 선택 (P1) — EXT-07 ~ EXT-09

| ID | 포맷 | 설명 | 선택 방법 |
|----|------|------|-----------|
| EXT-07 | **table** (기본) | README 예시와 동일한 텍스트 줄 출력 | `--format table` 또는 미지정 |
| EXT-08 | **json** | `[{"from": "...", "to": "...", "value": ...}, ...]` | `--format json` |
| EXT-09 | **csv** | `from_unit,from_value,to_unit,to_value` 헤더 + 행 | `--format csv` |

---

## 4. 비기능 요구사항 — NFR-04 ~ NFR-08

| ID | 요구사항 | PRD § |
|----|----------|-------|
| NFR-04 | Python 3.10+ | §4 |
| NFR-05 | 외부 의존성 최소화 (YAML 사용 시 `pyyaml` 허용) | §4 |
| NFR-06 | 변환 정확도: 내부 계산 float, TC 허용 오차 `1e-4` | §4 |
| NFR-07 | 검증 실패 시 exit code `1`, 정상 종료 `0` | §4 |
| NFR-08 | `python UnitConverter.py` (또는 `python -m src.cli`) 로 실행 가능 | §4 |

> **NFR-01 ~ NFR-03** (OCP, SRP, 테스트 가능성)은 §3.4 아키텍처 요구에 정의.

---

## 5. 레거시 코드 스멜 (`UnitConverter.py`)

PRD 구현 시 제거·리팩터링 대상 목록.

| # | 스멜 유형 | 현상 | 위치 |
|---|-----------|------|------|
| 1 | God Function / SRP 위반 | 입력·검증·변환·출력이 `main()` 한 함수에 모두 존재 | L1–32 |
| 2 | Magic Number 반복 | `3.28084`, `1.09361`이 4곳에 하드코딩 | L19–21, L27–28 |
| 3 | OCP 위반 | 단위 추가 시 `elif` 분기·출력 줄 모두 수정 필요 | L16–32 |
| 4 | 개방-확장 구조 부재 | 클래스·인터페이스·전략 패턴 없음 | 전체 |
| 5 | 테스트 불가능 | `input()`/`print()` 직접 결합 | L2, L30–32 |
| 6 | 중복 변수 | `meter_value`와 `in_meters` 동일 의미 | L26–27 |
| 7 | 불완전한 입력 검증 | 음수·빈 값·공백 trim 미처리 | L4–24 |
| 8 | 출력 정밀도 불일치 | README 예시(소수 1자리) vs 코드(전체 float) | L30–32 |
| 9 | 확장 포인트 부재 | 설정 외부화·동적 등록·출력 포맷 미구현 | — |
| 10 | I/O와 도메인 혼재 | CLI 프롬프트가 비즈니스 로직과 동일 레벨 | L2 |

---

## 6. PRD 갭 분석 (README vs 레거시 vs PRD 보완)

### 6.1 기능 갭

| # | README 요구 | 레거시 상태 | PRD 보완 |
|---|-------------|-------------|----------|
| F1 | OCP 설계 | if/elif + 하드코딩 | §3.4 Registry/인터페이스 |
| F2 | SRP 클래스 구성 | 단일 `main()` | §3.4 모듈 분리 |
| F3 | 음수 입력 검증 | 없음 | §3.3 Track A |
| F4 | 단위 변환 테스트 | 없음 | §7 수용 기준 |
| F5 | 설정 외부화 | 하드코딩 | §3.5 |
| F6 | 동적 단위 등록 | 없음 | §3.6 |
| F7 | 출력 포맷 선택 | 고정 print | §3.7 |
| F8 | meter 기반 파생 비율 | 상수 4곳 중복 | §3.2 Track B |

### 6.2 동작/UX 갭

| # | README | 레거시 | PRD 결정 |
|---|--------|--------|----------|
| U1 | `8.2 feet` (반올림) | 전체 float | 소수 1자리 반올림 |
| U2 | 다른 모든 단위 출력 | 소스 단위도 출력 | 소스 단위 제외 |
| U3 | `yard` 단수 | `yard` | 단수 유지 |
| U4 | `meter:2.5` | 동일 | trim 지원, 소문자만 |

### 6.3 PRD에서 명시적으로 정의한 항목 (README 모호함 해소)

| # | 항목 | PRD 결정 |
|---|------|----------|
| P1 | 동적 등록 UX | `--register` 또는 대화형 (MVP) |
| P2 | 설정 파일 | `config/units.json`, `--config` 옵션 |
| P3 | 출력 포맷 선택 | `--format {table\|json\|csv}` |
| P4 | 등록 단위 영속성 | 세션 한정 (Phase 2에서 파일 저장 검토) |
| P5 | 에러 처리 | 메시지 출력 + exit code 1 |
| P6 | 변환 정확도 | float, TC 허용 오차 1e-4 |
| P7 | 초기 단위 | meter/feet/yard + 확장 |
| P8 | 실행 방식 | CLI (`python UnitConverter.py`) |
| P9 | 대소문자 | 소문자만 (MVP) |

---

## 7. 수용 기준 (Acceptance Criteria)

### 7.1 P0 — MVP

- [ ] **Track B (Domain):** `meter:2.5` → feet, yard 변환 (소스 meter 제외, FR-02)
- [ ] **Track B (Domain):** 반올림 규칙 적용 — 8.2 feet, 2.7 yard (FR-03)
- [ ] **Track A (Boundary):** 잘못된 형식·숫자·음수·미지 단위 오류 메시지 (FR-06~09)
- [ ] **Track A (Boundary):** `meter:2.5` 파싱 — unit=meter, value=2.5 (FR-01)
- [ ] 새 단위 추가 시 Converter 핵심 로직 수정 없이 Registry만 확장 (NFR-01)
- [ ] `tests/test_converter.py`: meter↔feet, meter↔yard, feet↔yard (TC-FR-02~05)
- [ ] `tests/test_cli.py`: 입력 검증·파싱 (TC-FR-01, TC-FR-06~12)

### 7.2 P1 — 추가 요구

- [ ] `config/units.json`에서 비율 로드, `--config`로 경로 지정 가능
- [ ] `--register "cubit:0.4572"` 후 cubit 변환 가능
- [ ] `--format json|csv|table` 각 포맷 정상 출력
- [ ] 설정 파일·동적 등록·포맷 관련 TC

---

## 8. 테스트 추적표 (Requirements → Test Traceability Matrix)

PRD 요구사항(FR / NFR / EXT)과 테스트 케이스(Test ID)를 **1:1**로 매핑한다.  
`Req ID` → `Test ID` → `Test File` 경로로 **개념(PRD) → 코드(Test)** 까지 추적 가능하다.

### 8.1 추적 원칙

| 항목 | 규칙 |
|------|------|
| Req ID | FR(기능), NFR(비기능·아키텍처), EXT(확장/P1) |
| Track | **A (Boundary)** → `test_cli.py` / **B (Domain)** → `test_converter.py` |
| Test ID | `TC-{Req ID}` — 요구 1건당 테스트 1건 |
| Given / Then | pytest Given-When-Then 또는 Arrange-Assert 형태로 구현 |
| P | P0(MVP) / P1(추가 요구) |

### 8.2 FR — 기능 요구 (§3.2 Track B, §3.3 Track A)

#### Track B — Domain (`tests/test_converter.py`)

| Req ID | Track | Test ID | 요구 | Given | Then | P | Test File |
|--------|-------|---------|------|-------|------|---|-----------|
| FR-02 | B | TC-FR-02 | 전 단위 출력 | `meter:2.5`, 기본 Registry | feet·yard 변환 결과 반환, **meter 제외** | P0 | `tests/test_converter.py` |
| FR-03 | B | TC-FR-03 | 소수 1자리 반올림 | `meter:2.5` | `"8.2 feet"`, `"2.7 yard"` | P0 | `tests/test_converter.py` |
| FR-04 | B | TC-FR-04 | meter 기준 파생 변환 | `feet:3.28084` | `yard ≈ 1.0` (meter 경유) | P0 | `tests/test_converter.py` |
| FR-05 | B | TC-FR-05 | 단위 표기 (단수) | `meter:1` | 출력 단위명 `feet`, `yard` (복수형 아님) | P0 | `tests/test_converter.py` |

#### Track A — Boundary (`tests/test_cli.py`)

| Req ID | Track | Test ID | 요구 | Given | Then | P | Test File |
|--------|-------|---------|------|-------|------|---|-----------|
| FR-01 | A | TC-FR-01 | `meter:2.5` 파싱 | 유효 문자열 `"meter:2.5"` | `unit="meter"`, `value=2.5` | P0 | `tests/test_cli.py` |
| FR-06 | A | TC-FR-06 | 잘못된 형식 | `"meter"` (콜론 없음) | 형식 오류 메시지, 예외 또는 exit 1 | P0 | `tests/test_cli.py` |
| FR-07 | A | TC-FR-07 | 잘못된 숫자 | `meter:abc` | `Invalid number: abc` | P0 | `tests/test_cli.py` |
| FR-08 | A | TC-FR-08 | 음수 거부 | `meter:-1` | `Negative values are not allowed`, 거부 | P0 | `tests/test_cli.py` |
| FR-09 | A | TC-FR-09 | 미지 단위 | `cubit:1` (미등록) | `Unknown unit: cubit` | P0 | `tests/test_cli.py` |
| FR-10 | A | TC-FR-10 | 빈 unit/value | `":2.5"` 또는 `"meter:"` | empty format 오류 | P0 | `tests/test_cli.py` |
| FR-11 | A | TC-FR-11 | 공백 trim | `" meter : 2.5 "` | `unit="meter"`, `value=2.5` | P0 | `tests/test_cli.py` |
| FR-12 | A | TC-FR-12 | 대소문자 거부 | `Meter:2.5` | `Unknown unit: Meter` | P0 | `tests/test_cli.py` |

### 8.3 NFR — 비기능·아키텍처 요구 (§3.4, §4)

| Req ID | Test ID | 요구 | Given | Then | P | Test File |
|--------|---------|------|-------|------|---|-----------|
| NFR-01 | TC-NFR-01 | OCP | inch를 Registry에 등록 | Converter/Formatter **코드 비수정**, inch 변환 가능 | P0 | `tests/test_registry.py` |
| NFR-02 | TC-NFR-02 | SRP | — | Parser / Registry / Converter / Formatter **모듈 분리** | P0 | `tests/test_structure.py` |
| NFR-03 | TC-NFR-03 | 테스트 가능성 | Converter 단독 호출 | `input`/`print` 없이 pytest 실행 | P0 | `tests/test_converter.py` |
| NFR-04 | TC-NFR-04 | Python 3.10+ | 실행 환경 | `sys.version_info >= (3, 10)` | P0 | `tests/test_environment.py` |
| NFR-05 | TC-NFR-05 | 의존성 최소화 | `pip list` | stdlib + pytest (+ pyyaml 선택) | P1 | `tests/test_environment.py` |
| NFR-06 | TC-NFR-06 | 변환 정확도 | `meter:1` → feet | `abs(result - 3.28084) < 1e-4` | P0 | `tests/test_converter.py` |
| NFR-07 | TC-NFR-07 | exit code | 검증 실패 / 정상 입력 | 실패 `exit 1`, 성공 `exit 0` | P0 | `tests/test_cli.py` |
| NFR-08 | TC-NFR-08 | CLI 실행 | `python UnitConverter.py` + 입력 | 정상 변환 출력 | P0 | `tests/test_cli.py` |

### 8.4 EXT — 확장 요구 (§3.5 ~ §3.7)

| Req ID | Test ID | 요구 | Given | Then | P | Test File |
|--------|---------|------|-------|------|---|-----------|
| EXT-01 | TC-EXT-01 | 설정 파일 로드 | `config/units.json` | feet=3.28084, yard=1.09361 로드 | P1 | `tests/test_config_loader.py` |
| EXT-02 | TC-EXT-02 | 설정 누락 기본값 | 설정 파일 없음 | 내장 기본 비율 사용 | P1 | `tests/test_config_loader.py` |
| EXT-03 | TC-EXT-03 | 설정 파싱 실패 | malformed JSON | 오류 메시지, exit 1 | P1 | `tests/test_config_loader.py` |
| EXT-04 | TC-EXT-04 | `--config` 옵션 | `custom_units.json` | 지정 파일 비율 로드 | P1 | `tests/test_config_loader.py` |
| EXT-05 | TC-EXT-05 | 동적 등록 | `--register "cubit:0.4572"` | Registry에 cubit 등록 | P1 | `tests/test_registry.py` |
| EXT-06 | TC-EXT-06 | 등록 후 즉시 변환 | cubit 등록 후 `cubit:1` | meter 등 다른 단위로 변환 가능 | P1 | `tests/test_registry.py` |
| EXT-07 | TC-EXT-07 | table 포맷 | `--format table`, `meter:2.5` | 텍스트 줄 출력 | P1 | `tests/test_cli.py` |
| EXT-08 | TC-EXT-08 | json 포맷 | `--format json` | 유효 JSON 배열 | P1 | `tests/test_cli.py` |
| EXT-09 | TC-EXT-09 | csv 포맷 | `--format csv` | 헤더 + 행 CSV | P1 | `tests/test_cli.py` |

### 8.5 요약 매트릭스 (Req ID ↔ Test ID 1:1)

| 구분 | Track | Req ID 범위 | Test ID 범위 | Test File | 건수 | 우선순위 |
|------|-------|-------------|--------------|-----------|------|----------|
| FR (Domain) | B | FR-02 ~ FR-05 | TC-FR-02 ~ TC-FR-05 | `test_converter.py` | 4 | P0 |
| FR (Boundary) | A | FR-01, FR-06 ~ FR-12 | TC-FR-01, TC-FR-06 ~ TC-FR-12 | `test_cli.py` | 8 | P0 |
| NFR | — | NFR-01 ~ NFR-08 | TC-NFR-01 ~ TC-NFR-08 | (§8.3 참조) | 8 | P0/P1 |
| EXT | A/B | EXT-01 ~ EXT-09 | TC-EXT-01 ~ TC-EXT-09 | (§8.4 참조) | 9 | P1 |
| **FR 합계** | — | FR-01 ~ FR-12 | TC-FR-01 ~ TC-FR-12 | — | **12** | P0 |
| **전체 합계** | — | — | — | — | **29** | — |

### 8.6 Test File → Req ID 역추적 (FR Track)

| Test File | Track | 담당 FR / Test ID |
|-----------|-------|-------------------|
| `tests/test_converter.py` | **B (Domain)** | FR-02~05 → TC-FR-02~05, TC-NFR-03, TC-NFR-06 |
| `tests/test_cli.py` | **A (Boundary)** | FR-01, FR-06~12 → TC-FR-01, TC-FR-06~12, TC-NFR-07, TC-NFR-08, TC-EXT-07~09 |

### 8.7 Test File → Req ID 역추적 (NFR / EXT)

| Test File | 담당 Test ID |
|-----------|--------------|
| `tests/test_registry.py` | TC-NFR-01, TC-EXT-05, TC-EXT-06 |
| `tests/test_structure.py` | TC-NFR-02 |
| `tests/test_environment.py` | TC-NFR-04, TC-NFR-05 |
| `tests/test_config_loader.py` | TC-EXT-01 ~ TC-EXT-04 |

---

## 9. 구현 우선순위 및 일정 (Activities 6시간)

| Phase | 내용 | 예상 시간 | PRD 범위 |
|-------|------|-----------|----------|
| 1 | 문제 코드·요구사항 분석 | 0.5h | §5, §6 |
| 2 | P0: OCP/SRP 리팩터, Track A/B 분리 | 2h | §3.2–3.4 |
| 3 | P0: TC 작성 (test_cli / test_converter) | 0.5h | §7.1, §8.2–8.3 |
| 4 | P1: 설정·동적 등록·출력 포맷 + TC | 2h | §3.5–3.7, §7.2, §8.4 |
| 5 | 회고·발표 | 1h | — |

---

## 10. Out of Scope (Phase 2 이후)

- GUI / Web UI
- 길이 외 단위(무게, 온도 등)
- 동적 등록 단위의 파일 영속 저장
- 다국어 오류 메시지
- 대소문자 무시 단위명

---

## 11. 부록

### 11.1 레거시 코드 참조

```python
# UnitConverter.py — 핵심 변환 (하드코딩, OCP 위반)
if unit == "meter":
    meter_value = value
elif unit == "feet":
    meter_value = value / 3.28084
elif unit == "yard":
    meter_value = value / 1.09361
```

### 11.2 관련 문서

- [README.md](../README.md) — 원본 요구사항 및 실습 Activities
- [UnitConverter.py](../UnitConverter.py) — 레거시 시작 코드
