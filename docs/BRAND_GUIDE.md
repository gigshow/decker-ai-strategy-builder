# Decker AI Brand Guide

**목적**: 홍보·문서·채널에서 일관된 표현

---

## 네이밍

| 레벨 | 이름 | 용도 |
|------|------|------|
| **브랜드** | Decker AI | 전체 제품·서비스 |
| **제품** | Decker AI Strategy Builder | 시그널·룰북·라이프사이클 전략 빌더 |
| **에이전트** | DeckerClaw | 가재 마스코트. Decker 자체 에이전트 + OpenClaw 스킬 생태계 |

---

## DeckerClaw 포지셔닝 — 선택 기반 에이전트

> **에이전트 모델을 선택하면, 제공되는 아키텍처가 달라집니다.**

### 선택 A — Decker 자체 에이전트 (호스팅)
- **Telegram @deckerclawbot** — Decker 자체 개발 에이전트 (OpenClaw 미경유)
- 룰북 경로 LLM 토큰 $0. 결정론적 State Engine + RULES.yaml
- 비개발자·즉시 체험 사용자 대상

### 선택 B — OpenClaw 스킬 연동 (개발자)
- 자신의 OpenClaw에 **Decker 스킬(SKILL.md) 추가** → `web_fetch` → Decker API
- 사용자 OpenClaw에 Decker 에이전트 불필요. Decker API 서버만 호출
- Slack (제한 시 Telegram 우선), Discord 등 OpenClaw 지원 채널에서 사용 가능

### 선택 C — API 직접 (개발자)
- REST API로 시그널·전략·주문 직접 연동

### 입양 (Adopt DeckerClaw)
- **(A) 호스팅 사용**: [@deckerclawbot](https://t.me/deckerclawbot) 연동 — 가장 빠름
- **(B) OpenClaw 스킬 연동**: 자신의 OpenClaw에 Decker 스킬 추가 → web_fetch → API
- **(C) API 직접**: REST API 호출 — 개발자용

---

## 표현 규칙

| 상황 | 표현 |
|------|------|
| GitHub 레포 | `decker-ai-strategy-builder` |
| README 첫 문장 | "Decker AI Strategy Builder — deterministic signal lifecycle engine" |
| 텔레그램 | "@deckerclawbot (DeckerClaw)" — 자체 에이전트 |
| Slack·Discord | "OpenClaw 협업 (선택 B). Slack 제한 시 Telegram 우선" |
| API 문서 | "Decker AI API" |
| Medium | "Decker AI" 또는 "Decker AI Strategy Builder" |
| 입양 메시지 | "DeckerClaw 입양 = (A) Telegram 사용 (B) OpenClaw 스킬 연동 (C) API 직접" |

---

## 한 줄 핵심

> **Measure progress. Apply rules. No prediction.**

---

## 로고

| 용도 | 파일 | 컨셉 |
|------|------|------|
| **에이전트** | `assets/decker_claw_mascot_v1.png` | DeckerClaw, Decker와 협업 |
| **클라이언트** | `assets/decker_client_claw_*.png` | DeckerClaw + progress_pct (시그널 라이프사이클) |

---

## 참고

- [브랜딩_네이밍_홍보_작업계획_20250317.md](../../docs/브랜딩_네이밍_홍보_작업계획_20250317.md)
