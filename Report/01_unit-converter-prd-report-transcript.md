# PRD 작성 및 레거시 코드 갭 분석
_Exported on 6/5/2026 at 09:38:35 GMT+9 from Cursor (3.6.31)_

---

**User**

@README.md  를 참고하여   PRD를 작성하고자 합니다.
@README.md @UnitConverter.py 레거시코드스멜과PRD 갭을목록으로정리해줘.


---

**Cursor**

README와 `UnitConverter.py`를 읽고 프로젝트 구조를 확인한 뒤, 레거시 코드 스멜과 PRD 갭을 정리하겠습니다.


`README.md`가 목표 상태(요구사항)를 정의하고, `UnitConverter.py`는 37줄짜리 단일 스크립트 레거시입니다. PRD 작성에 바로 쓸 수 있도록 **레거시 코드 스멜**과 **PRD/README 갭**을 정리했습니다.

---

## 1. `UnitConverter.py` 레거시 코드 스멜

| # | 스멜 유형 | 현상 | 해당 코드 / 설명 |
|---|-----------|------|------------------|
| 1 | **God Function / SRP 위반** | 입력·검증·변환·출력이 `main()` 한 함수에 모두 있음 | ```1:32:c:\0604_AI\UnitConverter_02\UnitConverter.py``` |
| 2 | **Magic Number 반복** | `3.28084`, `1.09361`이 입력 변환·출력 변환에 각각 하드코딩 (총 4회) | ```16:28:c:\0604_AI\UnitConverter_02\UnitConverter.py``` |
| 3 | **OCP 위반 (Switch/If-Else 체인)** | 단위 추가 시 `elif` 분기와 출력 줄을 모두 수정해야 함 | ```16:32:c:\0604_AI\UnitConverter_02\UnitConverter.py``` |
| 4 | **개방-확장 구조 부재** | 클래스·인터페이스·전략 패턴 없음 — README의 OCP/SRP 요구와 정반대 | 전체 파일 |
| 5 | **테스트 불가능한 설계** | `input()` / `print()`에 직접 결합, 순수 변환 로직 분리 없음 | ```2:2```, ```30:32``` |
| 6 | **단일 책임·모듈 분리 없음** | 프로젝트에 `UnitConverter.py` 단일 파일만 존재 (테스트·설정 파일 없음) | 저장소 구조 |
| 7 | **중복 변수 / Dead naming** | `meter_value`와 `in_meters`가 동일 의미로 중복 | ```26:27:c:\0604_AI\UnitConverter_02\UnitConverter.py``` |
| 8 | **불완전한 입력 검증** | 형식·숫자·미지 단위만 처리; **음수 검증 없음** (README 품질 요구 미충족) | ```10:24``` |
| 9 | **엣지 케이스 미처리** | `meter:`, `:2.5`, 공백(`meter : 2.5`), 빈 입력 등 미정의 | ```8:8``` (`split`만 수행) |
| 10 | **출력 정밀도 불일치** | README 예시는 `8.2 feet`, `2.7 yard`(소수 1자리); 코드는 전체 float 출력 | README 34–36행 vs ```30:32``` |
| 11 | **확장 포인트 부재** | 외부 설정(JSON/YAML), 동적 단위 등록, 출력 포맷 선택 — README 추가 요구 전부 미구현 | README 58–64행 |
| 12 | **관심사 혼재 (I/O + 도메인)** | CLI 프롬프트 문자열이 비즈니스 로직과 같은 레벨에 존재 | ```2:2``` |

---

## 2. PRD 갭 (README 목표 vs 현재 구현 vs PRD에서 보완할 항목)

### A. 기능 갭 — README에 있으나 코드에 없음

| # | README 요구 | 현재 `UnitConverter.py` | PRD에 명시할 내용 |
|---|-------------|-------------------------|-------------------|
| F1 | OCP 설계 | if/elif + 하드코딩 | 단위별 변환기 인터페이스, 레지스트리/팩토리 구조 |
| F2 | SRP 클래스 구성 | 단일 `main()` 함수 | Parser / Validator / Converter / Formatter / Registry 역할 분리 |
| F3 | 음수 입력 검증 | 없음 | 음수 시 에러 메시지·종료 코드·재입력 여부 |
| F4 | 단위 변환 테스트 | 테스트 파일 없음 | pytest 등 TC 범위·정확도 허용 오차 |
| F5 | 설정 외부화 (JSON/YAML) | 비율 하드코딩 | 설정 파일 스키마, 기본값, 로드 실패 시 동작 |
| F6 | 동적 단위 등록 (`1 cubit = 0.4572 meter`) | 없음 | 등록 문법, 저장 위치(메모리/파일), 세션 지속 여부 |
| F7 | 출력 포맷 (JSON / CSV / 표) | 고정 `print` 텍스트 | 포맷 선택 방법(CLI 옵션·프롬프트), 각 포맷 스키마 |
| F8 | feet/yard 비율을 meter 기반 계산 | 개념은 맞으나 상수 4곳 중복 | **기준 단위(base unit) 1개** + 파생 비율 단일 정의 원칙 |

### B. 동작/UX 갭 — README 예시와 코드 동작 불일치

| # | README | 코드 | PRD 보완 필요 |
|---|--------|------|---------------|
| U1 | `2.5 meter = 8.2 feet` (반올림) | `8.2021...` 전체 출력 | 소수 자릿수·반올림 규칙 (예: 소수 1자리, banker's rounding 등) |
| U2 | 입력 단위 제외하고 “다른 모든 단위” 출력 | 입력 단위도 `meter` 줄로 다시 출력 | **소스 단위 포함/제외** 정책 |
| U3 | `yard` (단수) | `yard` 사용 | 단위 표기 규칙 (단수/복수, 약어) |
| U4 | `meter:2.5` 형식 | 동일 | 대소문자(`Meter`/`METER`), 공백 허용 여부 |

### C. PRD/README 자체의 모호함 (PRD 작성 시 반드시 정의)

README는 **무엇을** 만들지는 적혀 있지만, PRD에는 **어떻게**가 빠져 있습니다.

| # | 모호한 항목 | PRD에 정의할 질문 |
|---|-------------|-------------------|
| P1 | 동적 등록 UX | 별도 명령(`register cubit:0.4572 meter`)인지, 시작 시 설정 파일만인지 |
| P2 | 설정 파일 위치·이름 | `config.json` 기본 경로, CLI `--config` 지원 여부 |
| P3 | 출력 포맷 선택 | 실행 인자(`--format json`) vs 대화형 선택 |
| P4 | 등록 단위 영속성 | 프로그램 종료 후 유지 여부, `config`에 merge 여부 |
| P5 | 에러 처리 정책 | 검증 실패 시 exit code, 재시도, 로그 레벨 |
| P6 | 변환 정확도 | float 허용 vs `Decimal` 사용, TC 허용 오차 (예: `1e-6`) |
| P7 | 지원 단위 초기 목록 | meter/feet/yard 고정 + 확장만 vs 완전 사용자 정의 |
| P8 | 비기능 요구 | Python 최소 버전, 의존성(pyyaml 등), 디렉터리 구조 |
| P9 | CLI vs 라이브러리 | `python UnitConverter.py`만 vs import 가능 모듈 API |
| P10 | Activities(6h) 범위 | PRD MVP vs Phase 2(추가 요구) 우선순위·일정 매핑 |

---

## 3. PRD 작성용 요약 매트릭스

| 영역 | README | 레거시 | PRD 우선순위 |
|------|--------|--------|--------------|
| 핵심 변환 (meter/feet/yard) | ✅ | ⚠️ 동작은 함, 구조·정밀도 문제 | P0 — 리팩터 + 정밀도 규칙 |
| 입력 검증 (형식/숫자/단위) | ✅ | ⚠️ 부분 | P0 — 음수·엣지 케이스 추가 |
| OCP / SRP | ✅ | ❌ | P0 — 아키텍처 요구사항 |
| 단위 테스트 | ✅ | ❌ | P0 |
| 설정 외부화 | ✅ (추가) | ❌ | P1 |
| 동적 단위 등록 | ✅ (추가) | ❌ | P1 |
| 출력 포맷 선택 | ✅ (추가) | ❌ | P1 |

---

## 4. PRD 초안에 넣기 좋은 “현재→목표” 한 줄

> **As-Is:** 37줄 단일 스크립트, 하드코딩 비율, if/elif 분기, stdin/stdout 고정, 테스트·설정·확장 기능 없음.  
> **To-Be (README 기준):** 기준 단위 기반 확장 가능 변환 엔진 + 검증 계층 + 외부 설정 + 동적 등록 + 다중 출력 포맷 + 테스트로 보장된 정확도.

---

PRD 본문(목적, 사용자 스토리, 기능/비기능 요구, 수용 기준, MVP 범위) 초안까지 작성해 드릴 수 있습니다. Agent 모드로 전환하시면 파일로도 정리할 수 있습니다.

---

**User**

PRD  폴더를 만들어서 위 PRD md 파일로 저장

---

**Cursor**

PRD 폴더를 만들고 이전 분석을 바탕으로 PRD 마크다운 파일을 작성합니다.


`PRD` 폴더를 만들고 PRD 문서를 저장했습니다.

**경로:** [PRD/unit-converter-prd.md](c:\0604_AI\UnitConverter_02\PRD\unit-converter-prd.md)

문서에 포함된 내용:

1. **개요** — As-Is / To-Be, 목적
2. **사용자 스토리** — P0/P1 우선순위
3. **기능 요구사항** — 기본 변환, 입력 검증, OCP/SRP, 설정 외부화, 동적 등록, 출력 포맷
4. **비기능 요구사항** — Python 버전, 정확도, exit code
5. **레거시 코드 스멜** — `UnitConverter.py` 10항목
6. **PRD 갭 분석** — README vs 레거시 vs PRD 보완 결정
7. **수용 기준** — MVP(P0) / 추가(P1) 체크리스트
8. **일정** — README Activities 6시간 매핑
9. **Out of Scope** — Phase 2 항목

README에서 모호했던 항목(반올림 규칙, 소스 단위 출력 제외, 설정 스키마, CLI 옵션 등)도 PRD에서 명시해 두었습니다. 수정이나 영문 버전이 필요하면 알려주세요.

---

**User**

아래 예시를 참고하여 PRD → 테스트추적표를 만들어서 PRD 에 추가해주세요
모든FR / NFR 에테스트ID 를1:1 로매핑한다—개념(PRD)에서코드(Test)까지추적가능하게.
ID
요구
Given
Then
P
FR-01
meter:2.5 파싱
유효문자열
value=2.5, unit=meter
P0
FR-02
전단위출력
meter 2.5
feet≈8.2021, yard≈2.7340
P0
FR-03
미지단위
cubit:1 (미등록)
명확한오류
P0
FR-04
음수
meter:-1
거부/ 예외
P0
FR-05
잘못된형식
meter / abc
형식오류
P0
NFR-01
OCP
inch 추가
기존변환기코드비수정
P0
NFR-02
SRP
—
Parser / Registry / Converter / Printer 분리
P0
EXT-01
설정파일
units.json
비율로드
P1
EXT-02
동적등록
1 cubit = 0.4572 m
즉시변환가능
P1
EXT-03
출력포맷
--format
json / csv / table 포맷별검증
P1

---

**Cursor**

PRD의 FR/NFR을 확인한 뒤, 예시 형식에 맞춰 테스트 추적표를 작성해 PRD에 추가합니다.


PRD의 FR/NFR을 1:1 테스트 ID로 매핑한 추적표를 작성해 PRD에 추가하고, 요구사항 섹션에 ID를 부여합니다.


FR/NFR ID 표를 보강하고, 중복 `<details>` 블록을 제거한 뒤 테스트 추적표 섹션을 추가합니다.


PRD에 **§8 테스트 추적표**를 추가했습니다. 문서 버전은 1.1입니다.

### 추가 내용 요약

**§3 요구사항 ID 부여**
- `FR-01 ~ FR-12` — 기본 변환 + 입력 검증
- `NFR-01 ~ NFR-03` — OCP / SRP / 테스트 가능성 (§3.3)
- `NFR-04 ~ NFR-08` — Python 버전, 정확도, exit code 등 (§4)
- `EXT-01 ~ EXT-09` — 설정·동적 등록·출력 포맷 (P1)

**§8 테스트 추적표 (1:1 매핑)**

| 구분 | Req ID | Test ID | 건수 |
|------|--------|---------|------|
| FR | FR-01 ~ FR-12 | TC-FR-01 ~ TC-FR-12 | 12 |
| NFR | NFR-01 ~ NFR-08 | TC-NFR-01 ~ TC-NFR-08 | 8 |
| EXT | EXT-01 ~ EXT-09 | TC-EXT-01 ~ TC-EXT-09 | 9 |
| **합계** | — | — | **29** |

각 행에 **Given / Then / P / Test File**을 포함해 `Req ID → Test ID → tests/*.py` 경로로 PRD에서 테스트 코드까지 추적할 수 있습니다.

**§8.6**에는 Test File → Test ID 역추적표도 포함했습니다.

예시와의 대응:
- `FR-01` 파싱, `FR-02` 전 단위 출력, `FR-08` 음수, `FR-09` 미지 단위, `FR-06` 형식 오류
- `NFR-01` OCP, `NFR-02` SRP
- `EXT-01 ~ EXT-03` 설정·동적 등록·출력 포맷

파일: [PRD/unit-converter-prd.md](c:\0604_AI\UnitConverter_02\PRD\unit-converter-prd.md) §8 참고

---

**User**

지금 생성한 파일에 대하여 report파일을 만들고, Report폴더에 저장해줘
파일이름에는 01_ 로 시작하는 prefix를 추가해줘

---

**Cursor**

PRD 내용을 확인한 뒤 Report 폴더에 `01_` 접두사가 붙은 리포트 파일을 작성합니다.


Report 파일을 생성해 저장했습니다.

**경로:** [Report/01_unit-converter-prd-report.md](c:\0604_AI\UnitConverter_02\Report\01_unit-converter-prd-report.md)

### Report 구성

| § | 내용 |
|---|------|
| 1 | Report 목적 |
| 2 | 분석 대상 (README, UnitConverter.py, PRD) |
| 3 | PRD 문서 구조 요약 (§1~§11) |
| 4 | 요구사항 인벤토리 (FR 12 + NFR 8 + EXT 9 = 29건) |
| 5 | 레거시 코드 스멜 10건 요약 |
| 6 | README → PRD 갭 해소 현황 |
| 7 | 테스트 추적표 1:1 매핑 검증 (29:29) |
| 8 | 구현 우선순위 (Activities 6시간 연계) |
| 9 | 현재 구현 상태 (As-Is) |
| 10 | 결론 및 권장 다음 단계 |
| 11 | 관련 문서 링크 |

파일명은 요청하신 대로 `01_` prefix로 `01_unit-converter-prd-report.md`입니다.

