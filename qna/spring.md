# 🌱 Spring — Q&A 모음

출퇴근 때 푼 문제를 날짜순으로 쌓아요. 면접 직전에 이 파일만 훑어봐도 되게끔 모범답안은 짧게 정리해요.

<!-- 새 문제는 아래에 추가 -->

### 2026-11-25 — @Transactional 동작 원리
**Q. @Transactional을 붙이면 내부적으로 어떻게 트랜잭션이 처리되나요?**
- 빈마다 AOP 프록시가 생성되어 호출을 가로챔 → 트랜잭션 매니저가 커넥션을 받아 autoCommit=false, ThreadLocal에 보관해 같은 스레드의 Repository가 공유
- RuntimeException/Error면 롤백, 아니면 커밋 후 커넥션 반납

### 2026-11-25 — 내부 호출
**Q. 같은 클래스에서 this.B()로 @Transactional 메서드를 부르면?**
- 원본 객체의 this는 프록시가 아니라서 트랜잭션이 적용되지 않음 (B의 설정은 없는 것과 같음)
- 별도 빈으로 분리해서 해결. private 메서드도 같은 이유로 적용 안 됨

### 2026-11-25 — 롤백 규칙
**Q. Checked 예외가 나면 롤백되나요?**
- 기본은 커밋. Checked는 복구 가능한 비즈니스 예외, Unchecked/Error는 예상 못 한 오류로 보는 설계(EJB 관례)
- rollbackFor로 변경 가능

### 2026-11-25 — 전파 속성
**Q. REQUIRED vs REQUIRES_NEW?**
- REQUIRED(기본): 기존 트랜잭션에 참여, 없으면 생성
- REQUIRES_NEW: 기존을 보류하고 새 커넥션으로 독립 트랜잭션. 감사 로그 등에 사용
- 주의: 예외 전파는 별개라 바깥에서 잡아야 함, 커넥션 2개 사용으로 풀 고갈 위험

### 2026-11-25 — rollback-only
**Q. REQUIRED로 참여한 내부 메서드의 예외를 바깥에서 catch하면 커밋되나요?**
- 안 됨. 내부에서 물리 트랜잭션에 rollback-only가 표시되고, 바깥 커밋 시점에 롤백 + UnexpectedRollbackException
- 해결: 내부를 REQUIRES_NEW, 내부에서 예외 처리, noRollbackFor

### 2026-11-25 — readOnly
**Q. readOnly = true의 효과는?**
- JPA flush 생략(스냅샷·변경 감지 X)으로 성능 이점, JDBC 읽기 전용 힌트로 DB 최적화, 레플리카 라우팅 기준
- 엔티티 수정은 조용히 무시, 직접 쓰기 쿼리는 DB에 따라 에러

### 2026-11-25 — 프록시와 전파 (복습 꼬리 질문)
**Q. A에 @Transactional을 붙이면 this.B()가 A 트랜잭션에 얹히는데, 이게 전파인가요?**
- 아님. 전파는 프록시를 거쳐 호출될 때 적용되는 규칙. this.B()는 B의 어노테이션이 읽히지 않고, 같은 스레드의 ThreadLocal 커넥션을 쓰니 A 트랜잭션 안에 있을 뿐 → B의 REQUIRES_NEW 등은 무시
- 프록시는 클래스에 @Transactional 메서드가 하나라도 있으면 생성됨. TransactionTemplate은 프록시 없이 동작

### 2026-11-25 — REQUIRES_NEW와 커넥션 풀 데드락
**Q. REQUIRES_NEW를 쓸 때 트래픽이 몰리면 어떤 문제가 생기나요?**
- 요청 하나가 커넥션 2개 필요. 바깥 트랜잭션들이 풀을 다 잡으면 안쪽은 커넥션을 못 받고, 바깥은 안쪽이 끝나야 반납 → 커넥션 풀 데드락
- 풀 크기 산정, 바깥 트랜잭션 이후 처리(이벤트)로 구조 변경

### 2026-11-26 — @Transactional 동작 흐름 (키워드)
**Q. @Transactional 호출 시 내부 동작은?**
- AOP 프록시 → 트랜잭션 매니저 → 커넥션 풀에서 획득, autoCommit=false → ThreadLocal 바인딩 → 같은 스레드는 같은 커넥션 → 정상 commit / 예외 rollback → 반납
- 쿼리가 담기는 곳 = ThreadLocal에 묶인 같은 커넥션 (한 커넥션 = 한 DB 트랜잭션)

### 2026-11-26 — 전파 속성 기본값
**Q. REQUIRED가 기본값인가요? 전파 속성과 뭐가 다른가요?**
- 전파 속성은 선택지 전체의 이름, REQUIRED는 그중 기본값
- REQUIRES_NEW는 요청 하나가 커넥션 2개 → 풀 고갈 시 풀 데드락

### 2026-11-26 — readOnly와 flush·스냅샷
**Q. readOnly = true는 수정을 막기 위한 기능인가요? flush 생략은 무슨 뜻이죠?**
- 주목적은 최적화와 읽기 전용이라는 의도 표시. 수정 방지 장치가 아님(수정해도 조용히 반영만 안 됨)
- flush = 영속성 컨텍스트의 변경을 커밋 직전에 DB로 보내는 것. 자동 flush는 변경 감지(스냅샷 비교)를 포함, readOnly는 MANUAL이라 이를 생략
- 스냅샷은 조회로 영속성 컨텍스트에 올라오는 순간 최초 상태를 복사, flush 때 현재 값과 비교. readOnly는 스냅샷 자체를 안 만듦
