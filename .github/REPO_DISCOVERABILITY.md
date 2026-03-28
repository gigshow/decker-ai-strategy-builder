# GitHub 레포 검색 노출 설정

**목적**: Google·GitHub 검색에서 레포 발견 용이  
**적용**: GitHub 웹 UI에서 수동 설정 (레포 → About → Edit)

**지원 자산**: 암호화폐, 해외선물, 주식 (시세·시그널 제공 중, 향후 확장 예정)

---

## 1. About Description

**설정 위치**: 레포 메인 → 우측 About → ⚙️ Edit

**권장 문구** (한 줄, 350자 이내) — README 슬로건·Phase 4(시퀀스·FSM·게이트)와 정렬:

```
Decker — the market has grammar. Sequence labeling + 5-state FSM + GO/WATCH/HOLD + progress_pct & YAML rules. DeckerClaw (Telegram) + REST API. Deterministic structure, not price prediction.
```

또는 (한국어 About용):

```
시장에는 문법이 있다 — 시퀀스 라벨·상태머신·GO/WATCH/HOLD·progress_pct·룰북. 텔레그램 DeckerClaw·공개 API. 가격 예측이 아니라 결정론적 구조 엔진.
```

짧은 영문 버전:

```
Structural market engine: sequences → FSM → gate → RULES → optional LLM. progress_pct lifecycle. DeckerClaw + API.
```

---

## 2. Topics (태그)

**설정 위치**: About → Topics → Add topics

**권장 Topics** (소문자, 하이픈, 최대 20개):

| # | Topic | 검색어 |
|---|-------|--------|
| 1 | ai-trading | AI 트레이딩 |
| 2 | crypto-signal | 암호화폐 시그널 |
| 3 | trading-bot | 트레이딩 봇 |
| 4 | bitcoin | 비트코인 |
| 5 | ethereum | 이더리움 |
| 6 | cryptocurrency | 암호화폐 |
| 7 | futures | 해외선물 |
| 8 | stock-trading | 주식 |
| 9 | telegram-bot | 텔레그램 봇 |
| 10 | signal-engine | 시그널 엔진 |
| 11 | algorithmic-trading | 알고리즘 트레이딩 |
| 12 | trading-api | 트레이딩 API |
| 13 | market-analysis | 시장 분석 |
| 14 | python | Python 샘플 |
| 15 | yaml | RULES.yaml |
| 16 | trading-signals | 트레이딩 시그널 |
| 17 | state-machine | 상태 머신 |
| 18 | deterministic | 결정론적 엔진 |

**복사용** (쉼표 구분, 20개 제한 시 아래에서 2개 제거):
```
ai-trading, crypto-signal, trading-bot, bitcoin, ethereum, cryptocurrency, futures, stock-trading, telegram-bot, signal-engine, algorithmic-trading, trading-api, market-analysis, python, yaml, trading-signals, state-machine, deterministic
```

---

## 3. Website

**URL**: https://decker-ai.com

---

## 4. README SEO (적용됨)

- HTML 주석에 keywords 추가
- Overview 하단에 검색어 라인 추가

---

## 5. 적용 체크리스트

- [ ] About Description 설정
- [ ] Topics 16개 추가 (crypto, futures, stocks 포함)
- [ ] Website URL 확인
- [ ] 1~2일 후 Google에서 "decker ai trading" 검색 테스트
