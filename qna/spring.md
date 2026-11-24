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
