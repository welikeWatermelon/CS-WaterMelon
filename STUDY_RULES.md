# 📏 학습 루틴 규칙

Claude가 매일 이 repo를 업데이트할 때 따르는 규칙이에요.

## 하루 흐름 (편도 30분 내외)

| 시간 | 할 일 |
|---|---|
| 🚇 출근 | 그날 고른 과목에서 **문제 풀이 위주** (5~8문제). 모르는 건 바로 개념 설명 |
| 🏠 퇴근 | **오답노트 + 며칠 전 주제 복습 문제** 3~5개, 시간이 남으면 새 문제 |

- 과목을 정하지 않으면 `roadmap.md`에서 **가장 오래 안 본 과목**의 다음 주제를 추천
- 문제 형식: 면접 질문형(서술) 위주, 가끔 객관식·코드 읽기·"이 상황이면 어떻게?" 설계형
- 채점: ✅ 정답 / 🔺 부분 정답 / ❌ 오답

## 파일 업데이트 규칙

| 파일 | 언제 | 내용 |
|---|---|---|
| `logs/YYYY/MM/YYYY-MM-DD.md` | 매 세션 | 그날 문제, 내 답, 채점, 보충 설명 (front matter 필수) |
| `qna/<과목>.md` | 매 세션 | 그날 문제를 과목 파일에 누적 (질문 + 모범답안 요약) |
| `review/wrong-notes.md` | ❌·🔺 나올 때 | 오답 추가 / 복습에서 맞히면 ✅로 졸업 |
| `concepts/<과목>/<주제>.md` | 새 개념 정리할 때 | 개념 원본. 아티팩트(개념 사전)도 같이 갱신 |
| `roadmap.md` | 주제를 충분히 다뤘을 때 | `[ ]` → `[x]` |
| `README.md`, `assets/heatmap.svg` | 매 커밋 전 | `python scripts/update_readme.py` 실행으로 자동 갱신 |

## 로그 front matter

```yaml
---
date: 2026-11-25
subjects: [db, spring]   # os, network, db, java, spring, infra, system-design
questions: 8
correct: 6               # ✅만 카운트
---
```

## 커밋 규칙

- author: `welikeWatermelon <bill5500@naver.com>` (잔디 반영용)
- 브랜치: `main`에 바로 커밋
- 메시지: `study(db,spring): 2026-11-25 출근 — 인덱스 6/8`
- 출근·퇴근 각각 커밋해도 되고, 하루 한 번 몰아서 해도 돼요
