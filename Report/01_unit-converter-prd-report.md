# 01 — Unit Converter PRD 생성 Report

| 항목 | 내용 |
|------|------|
| Report ID | 01 |
| 작성일 | 2026-06-05 |
| 대상 문서 | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| 문서 버전 | PRD v1.1 |
| 상태 | Complete |

---

## 1. Report 목적

본 Report는 `README.md`와 레거시 `UnitConverter.py`를 분석하여 작성된 **Product Requirements Document(PRD)** 의 생성 결과를 요약·검증한다.

- PRD 문서의 구조와 범위를 한눈에 파악할 수 있도록 한다.
- 레거시 코드 스멜과 README 대비 갭 분석 결과를 기록한다.
- FR / NFR / EXT 요구사항과 테스트 케이스(TC) 간 **1:1 추적 가능성**을 확인한다.
- 이후 구현·테스트 단계의 진입점으로 활용한다.

---

## 2. 분석 대상

| 구분 | 경로 | 역할 |
|------|------|------|
| 원본 요구 | [README.md](../README.md) | 기본·품질·추가 요구사항, 실습 Activities |
| 레거시 코드 | [UnitConverter.py](../UnitConverter.py) | As-Is 시작점 (37줄 단일 스크립트) |
| 산출물 | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) | To-Be 요구사항·수용기준·테스트 추적표 |

---

## 3. PRD 문서 구조 요약

| § | 섹션 | 내용 | 항목 수 |
|---|------|------|---------|
| 1 | 개요 | 목적, 배경, As-Is → To-Be | — |
| 2 | 사용자·시나리오 | 사용자 스토리 US-01 ~ US-06 | 6 |
| 3 | 기능 요구 | FR-01~12, NFR-01~03, EXT-01~09 | 29 |
| 4 | 비기능 요구 | NFR-04 ~ NFR-08 | 5 |
| 5 | 레거시 코드 스멜 | UnitConverter.py 리팩터 대상 | 10 |
| 6 | PRD 갭 분석 | README vs 레거시 vs PRD 결정 | 21 |
| 7 | 수용 기준 | P0 MVP / P1 추가 체크리스트 | 10 |
| 8 | 테스트 추적표 | Req ID ↔ Test ID 1:1 매핑 | 29 |
| 9 | 일정 | Activities 6시간 Phase 매핑 | 5 Phase |
| 10 | Out of Scope | Phase 2 이후 | 5 |
| 11 | 부록 | 레거시 코드·관련 문서 | — |

**총 페이지 분량:** PRD 406 lines (v1.1)

---

## 4. 요구사항 인벤토리

### 4.1 기능 요구 (FR) — P0

| ID | 요구 | PRD § |
|----|------|-------|
| FR-01 | 입력 파싱 (`unit:value`) | §3.1 |
| FR-02 | 전 단위 변환 출력 (소스 제외) | §3.1 |
| FR-03 | 소수 1자리 반올림 | §3.1 |
| FR-04 | meter 기준 파생 변환 | §3.1 |
| FR-05 | 단위 표기 (단수형) | §3.1 |
| FR-06 | 형식 검증 (`:` 필수) | §3.2 |
| FR-07 | 숫자 검증 | §3.2 |
| FR-08 | 음수 거부 | §3.2 |
| FR-09 | 미지 단위 거부 | §3.2 |
| FR-10 | 빈 unit/value 거부 | §3.2 |
| FR-11 | 공백 trim | §3.2 |
| FR-12 | 대소문자 (소문자만) | §3.2 |

### 4.2 비기능·아키텍처 요구 (NFR)

| ID | 요구 | 우선순위 | PRD § |
|----|------|----------|-------|
| NFR-01 | OCP (Registry 확장) | P0 | §3.3 |
| NFR-02 | SRP (모듈 분리) | P0 | §3.3 |
| NFR-03 | 테스트 가능성 (I/O 분리) | P0 | §3.3 |
| NFR-04 | Python 3.10+ | P0 | §4 |
| NFR-05 | 의존성 최소화 | P1 | §4 |
| NFR-06 | 변환 정확도 (허용 오차 1e-4) | P0 | §4 |
| NFR-07 | exit code 0/1 | P0 | §4 |
| NFR-08 | CLI 실행 | P0 | §4 |

### 4.3 확장 요구 (EXT) — P1

| ID | 요구 | PRD § |
|----|------|-------|
| EXT-01 | 설정 파일 로드 | §3.4 |
| EXT-02 | 설정 누락 시 기본값 | §3.4 |
| EXT-03 | 설정 파싱 실패 처리 | §3.4 |
| EXT-04 | `--config` 옵션 | §3.4 |
| EXT-05 | 동적 단위 등록 | §3.5 |
| EXT-06 | 등록 후 즉시 변환 | §3.5 |
| EXT-07 | table 출력 포맷 | §3.6 |
| EXT-08 | json 출력 포맷 | §3.6 |
| EXT-09 | csv 출력 포맷 | §3.6 |

**요구사항 합계:** FR 12 + NFR 8 + EXT 9 = **29건**

---

## 5. 레거시 코드 스멜 요약

`UnitConverter.py`에서 PRD 구현 시 해소해야 할 주요 스멜 10건을 PRD §5에 문서화했다.

| 우선순위 | 스멜 | 영향 | 대응 PRD |
|----------|------|------|----------|
| 높음 | God Function / SRP 위반 | 테스트·확장 불가 | NFR-02, §3.3 |
| 높음 | OCP 위반 (if/elif) | 단위 추가 시 전면 수정 | NFR-01, §3.3 |
| 높음 | Magic Number 4회 중복 | 비율 불일치 위험 | FR-04, EXT-01 |
| 높음 | 테스트 불가능 (I/O 결합) | TC 작성 불가 | NFR-03 |
| 중간 | 음수·빈값·trim 미처리 | 품질 요구 미충족 | FR-08, FR-10, FR-11 |
| 중간 | 출력 정밀도 불일치 | README 예시와 불일치 | FR-03 |
| 중간 | 확장 포인트 부재 | P1 요구 전부 미구현 | EXT-01~09 |
| 낮음 | 중복 변수 (`meter_value`/`in_meters`) | 가독성 | SRP 리팩터 시 제거 |
| 낮음 | I/O·도메인 혼재 | 유지보수성 | §3.3 모듈 분리 |

---

## 6. README → PRD 갭 해소 현황

README에 명시되었으나 모호하거나 레거시에 없던 항목을 PRD에서 구체화했다.

| README 갭 | PRD 결정 | § |
|-----------|----------|---|
| 반올림 규칙 미정 | 소수 1자리, round half up | §3.1 |
| 소스 단위 출력 여부 | 소스 단위 **제외** | §3.1 |
| 음수 처리 | 명시적 거부 + 메시지 | §3.2 FR-08 |
| OCP/SRP | 모듈 구조·Registry 패턴 | §3.3 |
| 설정 파일 스키마 | JSON 예시 + base_unit 정의 | §3.4 |
| 동적 등록 UX | `--register "cubit:0.4572"` | §3.5 |
| 출력 포맷 선택 | `--format {table\|json\|csv}` | §3.6 |
| 등록 단위 영속성 | 세션 한정 (Phase 2) | §6.3 P4 |

**갭 해소율:** README 핵심 요구 8/8 항목 PRD에 반영 완료

---

## 7. 테스트 추적표 (§8) 검증 결과

### 7.1 1:1 매핑 검증

| 구분 | Req ID | Test ID | 매핑 | 건수 |
|------|--------|---------|------|------|
| FR | FR-01 ~ FR-12 | TC-FR-01 ~ TC-FR-12 | 1:1 | 12 |
| NFR | NFR-01 ~ NFR-08 | TC-NFR-01 ~ TC-NFR-08 | 1:1 | 8 |
| EXT | EXT-01 ~ EXT-09 | TC-EXT-01 ~ TC-EXT-09 | 1:1 | 9 |
| **합계** | — | — | **29:29** | **29** |

**검증 결과:** 모든 FR / NFR / EXT 요구사항에 Test ID가 1:1로 할당됨. 누락·중복 없음.

### 7.2 추적 경로

```
PRD Req ID  →  Test ID  →  Test File  →  (구현) Source Code
   FR-01    →  TC-FR-01  →  test_parser.py
   NFR-01   →  TC-NFR-01 →  test_registry.py
   EXT-01   →  TC-EXT-01 →  test_config_loader.py
```

### 7.3 예정 Test File (9개)

| Test File | TC 건수 | 담당 범위 |
|-----------|---------|-----------|
| `tests/test_parser.py` | 2 | 파싱, trim |
| `tests/test_validator.py` | 6 | 입력 검증 |
| `tests/test_converter.py` | 4 | 변환, 정확도, 테스트 가능성 |
| `tests/test_formatter.py` | 5 | 반올림, 표기, 출력 포맷 |
| `tests/test_registry.py` | 3 | OCP, 동적 등록 |
| `tests/test_structure.py` | 1 | SRP 모듈 분리 |
| `tests/test_environment.py` | 2 | Python 버전, 의존성 |
| `tests/test_cli.py` | 2 | exit code, CLI 실행 |
| `tests/test_config_loader.py` | 4 | 설정 외부화 |

**예정 TC 합계:** 29건 (Req ID와 동일)

---

## 8. 구현 우선순위 (PRD §9 연계)

| Phase | 시간 | 범위 | TC |
|-------|------|------|-----|
| 1. 분석 | 0.5h | §5, §6 | — |
| 2. P0 구현 | 2h | FR-01~12, NFR-01~03 | — |
| 3. P0 TC | 0.5h | §7.1 | TC-FR-*, TC-NFR-01~04,06~08 |
| 4. P1 구현+TC | 2h | EXT-01~09, NFR-05 | TC-EXT-*, TC-NFR-05 |
| 5. 회고 | 1h | — | — |

---

## 9. 현재 구현 상태 (As-Is)

| 영역 | PRD 요구 | 현재 코드 | 상태 |
|------|----------|-----------|------|
| 기본 변환 | FR-01~05 | 부분 동작 (구조 미흡) | ⚠️ |
| 입력 검증 | FR-06~12 | 형식·숫자·단위만 | ⚠️ |
| OCP / SRP | NFR-01~02 | 미구현 | ❌ |
| 테스트 | NFR-03, §8 | tests/ 없음 | ❌ |
| 설정 외부화 | EXT-01~04 | 미구현 | ❌ |
| 동적 등록 | EXT-05~06 | 미구현 | ❌ |
| 출력 포맷 | EXT-07~09 | 미구현 | ❌ |

**PRD 대비 구현 완료율:** 0% (문서화 완료, 코드 구현 전)

---

## 10. 결론 및 권장 다음 단계

### 10.1 결론

1. PRD v1.1은 README 요구를 **29개 식별 가능한 Req ID**로 분해했다.
2. 레거시 `UnitConverter.py`의 **10개 코드 스멜**과 **8개 기능 갭**을 문서화했다.
3. README의 모호한 항목 **9건**을 PRD에서 명시적 결정으로 해소했다.
4. **29개 Test ID**와 **9개 Test File**로 PRD → Test → Code 추적 체계를 수립했다.

### 10.2 권장 다음 단계

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 1 | `src/` 모듈 골격 생성 | parser, validator, registry, converter, formatter, cli |
| 2 | P0 TC 선행 작성 (Red) | `tests/test_*.py` 20건 (FR + NFR P0) |
| 3 | P0 기능 구현 (Green) | FR-01~12, NFR-01~04,06~08 |
| 4 | `config/units.json` + P1 구현 | EXT-01~09 |
| 5 | P1 TC 작성·통과 | TC-EXT-*, TC-NFR-05 |
| 6 | Report 02 — 구현 완료 검증 | TC 통과율, PRD 수용 기준 체크 |

---

## 11. 관련 문서

| 문서 | 경로 |
|------|------|
| PRD (본 Report 대상) | [PRD/unit-converter-prd.md](../PRD/unit-converter-prd.md) |
| README (원본 요구) | [README.md](../README.md) |
| 레거시 코드 | [UnitConverter.py](../UnitConverter.py) |
