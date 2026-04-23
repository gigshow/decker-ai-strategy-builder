# 텔레그램 에이전트 — `/` 명령·자연어 대응

**목적**: 봇에서 **슬래시 명령**과 **자연어**가 같은 기능으로 동작함을 문서화한다.  
**구현**: `app/api/v1/endpoints/telegram_webhook.py` — `_dispatch_slash_command`

**원칙**

- `/명령`은 텔레그램 입력창에서 빠르게 호출할 때 쓴다.
- 동일 기능은 **한글·영문 자연어**로도 요청 가능 (기존 키워드 분기).
- 알 수 없는 `/foo` → `/help`·`/services` 안내 문구.

---

## 1. 안내·온보딩

| `/` 명령 | 별칭 | 자연어 예 | 설명 |
|----------|------|-----------|------|
| `/help` | `/usage`, `/h` | 하이, 뭐 할 수 있어, 영어 **`help`** 단독 ( `/help` 와 동일) | 핵심 사용법 |
| `/services` | `/service_list`, `/servicelist` | 서비스 리스트, service list | 11개 기능 목록 |
| `/link` | `/signup`, `/connect` | 사용법, 가입, 연동 | 가입·연동 3단계 |
| `/quest` | `/steps`, `/onboarding`, `/guide` | 단계별로 알려줘 | 5단계 체험 가이드 |
| `/where` | `/channels`, `/agent_vs_web` | 어디서 할 수 있어 | 텔레그램 vs 웹 |
| `/welcome` | — | — | 환영 메시지 |
| `/portfolio_reset` | `/reset` | 포트폴리오 리셋 | 대시보드 안내 |
| `/news_help` | `/news_distinction` | 뉴스 (단독) | 즉시 뉴스 vs 다이제스트 구분 |

---

## 2. 시장·시그널·포지션 (연동 시 일부 필수)

| `/` 명령 | 별칭 | 자연어 예 | 설명 |
|----------|------|-----------|------|
| `/position` | `/portfolio`, `/positions`, `/balances` | 포지션 보여줘 | 포트폴리오 (연동 필요) |
| `/signal` | `/signals` | 시그널 알려줘 | 시그널 요약 |
| `/signal_pos` | `/positions_signal` | 포지션별 시그널 | 시그널+포지션 개요 |
| `/price` | `/quote`, `/p` | 비트코인 얼마 | 시세 (`/price`만 보내면 기본 BTC) |
| `/market` | `/market_status` | 시장 상태 어때 | 시장 상태·바이어스 |
| `/compare` | `/cmp` | 비트 이더 비교 | 종목 비교 (인자 없으면 기본 문구) |
| `/poly` | `/polymarket` | 폴리마켓 | 폴리마켓 브리핑 |
| `/news` | `/digest` | 뉴스 (맥락) | 다이제스트 안내 (연동 여부에 따라 문구) |
| `/news_now` | `/newsnow` | 뉴스 보여줘 | 즉시 뉴스 (연동 필요) |

---

## 3. 개발자 API

| `/` 명령 | 별칭 | 자연어 예 | 설명 |
|----------|------|-----------|------|
| `/apikey` | `/api_key`, `/getkey`, `/mykey` | API 키 발급해줘 | Public API 키(`dk_live_xxx`) 발급·조회 (연동 필요) |
| `/apikey reset` | — | API 키 재발급 | 기존 키 폐기 후 새 키 발급 |

**흐름**: 연동 완료 → `/apikey` → `dk_live_xxx` 수령 → `X-API-Key` 헤더로 API 호출  
**문서**: [DEVELOPER_API_GUIDE.md](./DEVELOPER_API_GUIDE.md)

---

## 4. 디버그·메타

| `/` 명령 | 별칭 | 자연어 예 |
|----------|------|-----------|
| `/myid` | `/tg_id`, `/telegram_id` | 내 telegram id |
| `/chatid` | `/chat_id` | 채널 id |

---

## 5. 에이전트·IDE 스킬과의 관계

- **텔레그램 `/`**: 위 표 — 제품 봇 UX.
- **IDE `decker-*` 스킬** (`.cursor/skills/`): 코드·도메인 작업 (`docs/DECKER_AGENT_SKILLS.md`).
- 둘 다 “명령으로 빠르게 진입”이라는 점만 공유하고, **목록은 별도**로 유지한다.

---

## 6. 채널 구분 — 웹 PhaseD 채팅 vs 텔레그램

| 채널 | 위치 | 명령·트리거 | 비고 |
|------|------|-------------|------|
| **텔레그램 봇** | `telegram_webhook.py` | 위 §1~3 `/` + 자연어 키워드 | **정본**. 사용자용 시그널·주문·뉴스 등 |
| **웹 service-page (PhaseD)** | `src/decker/frontend/service-page/src/utils/chatCommandHandler.ts` | `/help`, `/services`, `/link` + 한글 `/상태`, `/포트폴리오` 등 | **P1**: `/help`·`/services`는 텔레그램과 **역할 정합** (문구는 웹용 요약 `WEB_PHASED_*`) |
| **IDE 스킬** | `.cursor/skills/decker-*` | 스킬 설명·도메인 링크 | 개발자용 |

- 웹 채팅 명령을 텔레그램과 맞추려면 **별 이슈**로 설계·QA (현재는 문서로만 역할 분리).
- PhaseD에서 `/help`를 넣을 경우 **텔레그램 `/help`와 동일 문구**를 쓸지는 제품 결정 사항.

---

## 6. 배포 정본 · `railway_sync`

- **정본(canonical)**: `src/decker/api/app/api/v1/endpoints/telegram_webhook.py` (슬래시 디스패치·키워드 전체).
- **`railway_sync/backend_latest/.../telegram_webhook.py`**: Railway/배포용 **미러**로 둘 수 있음 — **기능이 뒤처질 수 있음**. 릴리즈 전에 정본과 diff 검토 또는 `CONFIRM=1 ./scripts/sync_railway_telegram_webhook.sh` 로 정본 덮어쓰기(⚠️ 미리 diff 확인).
- OpenClaw·외부 패키지에 명령표를 실을 때는 **`docs/TELEGRAM_AGENT_COMMANDS.md`** 를 복사·요약한다.

---

## 7. 봇 메뉴 (입력창 `/` 힌트) — `setMyCommands`

텔레그램 클라이언트에 보이는 **슬래시 메뉴**는 Bot API **`setMyCommands`** 로 등록된다. 웹훅 코드(`_dispatch_slash_command`)와 **별개**이지만, **API 서버는 `TELEGRAM_BOT_TOKEN`이 있으면 기동 시마다** `telegram_bot_menu_commands` 정본으로 `setMyCommands`를 돌린다 (배포 = 메뉴 갱신). 예전 스코프에 남은 `send`, `reset` 등은 **`deleteMyCommands` 후 `setMyCommands`** 로 제거한다.

구현은 **`default`** 와 **`all_private_chats`** 두 스코프 모두에 같은 목록을 올린다 (일부 클라이언트는 한쪽만 반영).

| 항목 | 경로 |
|------|------|
| 메뉴에 올릴 목록 (정본) | `app/services/telegram_bot_menu_commands.py` — `DECKER_TELEGRAM_BOT_COMMANDS` |
| API 래퍼 | `app/services/telegram_bot_menu_sync.py` |
| 동기화 스크립트 | `scripts/set_telegram_bot_commands.py` |

**수동 반영 (토큰 필요):**

```bash
export TELEGRAM_BOT_TOKEN="..."   # 반드시 @deckerclawbot 에 연결된 봇 토큰
python scripts/set_telegram_bot_commands.py          # delete 후 set (권장)
python scripts/set_telegram_bot_commands.py --show   # API에 뭐가 올라갔는지 확인
python scripts/set_telegram_bot_commands.py --dry-run
```

- 메뉴가 여전히 옛날이면: 앱에서 채팅 나갔다 들어가기, 또는 `--show` 로 `getMyCommands` 결과가 Decker 목록인지 확인 (토큰이 다른 봇이면 목록이 안 맞음).

**배포 시 자동 반영:**

- Railway 등에 **`TELEGRAM_BOT_TOKEN`** 만 있으면 됨 — 재배포 시 `sync_decker_bot_menu_on_startup` 가 백그라운드에서 동기화.
- CI·로컬에서 프로덕 토큰으로 **실봇 메뉴를 건드리면 안 될 때** `TELEGRAM_SKIP_BOT_COMMANDS_SYNC=1`.

**명령 추가·변경 시:** `_dispatch_slash_command` + 이 문서 §1~3 + **`telegram_bot_menu_commands.py`** + 재배포 (또는 수동 스크립트).

---

*명령 추가 시: `telegram_webhook.py`의 `_dispatch_slash_command`, 이 표, **`telegram_bot_menu_commands.py`**, 그리고 필요 시 `set_telegram_bot_commands.py` 실행까지 함께 갱신할 것.*
