# ❌ 오답노트

틀렸거나(❌) 애매했던(🔺) 문제를 모아두는 곳이에요.
퇴근길 복습에서 다시 풀고, 맞히면 **졸업** 섹션으로 옮겨요.

## 📝 복습 대기

| 날짜 | 과목 | 질문 | 놓친 포인트 | 재도전 |
|---|---|---|---|---|
| 2026-11-24 | db | 인덱스가 있는데 풀스캔이 일어나는 경우는? | 옵티마이저가 풀스캔을 고르는 이유(선택도, 랜덤 I/O vs 순차 I/O), 컬럼 가공·형변환·복합 인덱스 선두 컬럼 | 11-25 🔺 |
| 2026-11-24 | db | DB 인덱스는 왜 B+Tree로 구현할까? | 리프에만 데이터 + 리프 연결 리스트(범위 검색), 중간 노드 키만 → fan-out↑ 높이↓ I/O↓ | 11-25 🔺 |
| 2026-11-25 | spring | @Transactional은 내부적으로 어떻게 동작하나? | AOP 프록시 → 트랜잭션 매니저 → autoCommit=false, ThreadLocal 커넥션 공유 → 커밋/롤백 | |
| 2026-11-25 | spring | Checked 예외 시 롤백? 왜? | Checked=복구 가능한 비즈니스 예외라 커밋, Unchecked=예상 못 한 오류라 롤백 | |
| 2026-11-25 | spring | REQUIRED vs REQUIRES_NEW | REQUIRED=있으면 참여/없으면 생성, REQUIRES_NEW=보류+새 커넥션. 커넥션 풀 데드락 주의 | 11-25 🔺 |
| 2026-11-25 | spring | REQUIRED 내부 예외를 바깥에서 catch하면 커밋? | rollback-only 표시 → 전체 롤백 + UnexpectedRollbackException | 11-25 🔺 |
| 2026-11-25 | spring | readOnly = true의 효과 | JPA flush·변경 감지 생략, DB 읽기 전용 최적화, 레플리카 라우팅 | |
| 2026-11-26 | java | `.java`가 실행되기까지 JVM 구조는? | 머신=가상 컴퓨터, javac→클래스 로더→Runtime Data Area(Heap/Stack/Method Area)→실행 엔진(인터프리터+JIT, GC) | |
| 2026-11-26 | java | `Person p = new Person()`에서 p와 객체의 위치는? | 참조 변수 p는 Stack, 객체는 Heap | |
| 2026-11-26 | java | GC는 안 쓰는 객체를 어떻게 판단? Young/Old 이유는? | 시간이 아니라 GC Root 도달 가능성, static도 Root, 약한 세대 가설, age 임계값 후 Old 승격 | |
| 2026-11-26 | java | Stop-The-World란? | GC 중 앱 스레드 전체 정지 → 응답 지연, G1/ZGC는 STW를 줄이는 방향 | |
| 2026-11-26 | java | 서버가 가끔 멈출 때 GC 원인이면 뭘 확인? | GC 로그의 pause·Full GC 빈도·청소 후 Old 사용량, jstat, 힙 덤프(MAT) | |
| 2026-11-26 | java | equals가 true면 hashCode도 같아야 하는 이유는? | HashMap이 hashCode로 버킷 → equals로 확인. 다르면 다른 버킷이라 조회 실패·중복 | |
| 2026-11-26 | java | String은 왜 불변인가? | Pool 공유는 불변이라서 가능 + HashMap 키 안전, 스레드 안전, 보안 | |


## 🎓 졸업

| 처음 틀린 날 | 졸업한 날 | 과목 | 질문 |
|---|---|---|---|
| 2026-11-25 | 2026-11-25 | spring | 같은 클래스 this.B() 호출 시 트랜잭션 적용? |
