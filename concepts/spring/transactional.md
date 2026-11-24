# @Transactional 동작 원리

## 한 줄 요약

`@Transactional`은 **AOP 프록시**가 메서드 호출을 가로채서, 커넥션의 auto-commit을 끄고 ThreadLocal로 커넥션을 공유하다가 결과에 따라 커밋하거나 롤백하는 방식으로 동작해요.

## 프록시의 역할

`@Transactional`이 붙은 빈 대신 컨테이너에 등록되는 대리 객체예요. 앱 시작 때 **빈마다 1개** 만들어지고 모든 요청이 공유해요.

```
[Controller] → [OrderService 프록시] → [OrderService 원본]
```

1. **시작**: 트랜잭션 매니저가 커넥션 풀에서 커넥션을 받아 `autoCommit = false`로 설정하고 ThreadLocal에 보관해요. 같은 스레드의 Repository들은 이 커넥션을 같이 써요.
2. **전파 판단**: 이미 트랜잭션이 있으면 전파 속성에 따라 참여할지 새로 만들지 정해요.
3. **위임**: 원본 메서드를 호출해요. 쿼리는 즉시 DB로 가지만 확정되지 않은 상태로 남아요.
4. **종료**: 정상 종료면 `commit`, RuntimeException/Error면 `rollback`. 커넥션은 풀에 반납해요.

> 쿼리를 앱에서 모아두는 게 아니에요. DB가 미확정 변경을 들고 있다가(Undo 로그) 커밋 때 확정해요. JPA의 쓰기 지연(flush 전까지 SQL을 모아둠)은 별개 기능이에요.

## 프록시를 안 거치면 트랜잭션이 안 먹어요

```java
public void A() { this.B(); }      // this = 원본 → B의 프록시를 안 거침
@Transactional public void B() { ... }
```

- A에 트랜잭션이 **없으면**: B는 auto-commit으로 쿼리마다 커밋 → 예외가 나도 롤백 안 됨
- A에 트랜잭션이 **있으면**: B는 A에 얹혀 실행되지만 B에 붙인 설정(REQUIRES_NEW, readOnly, rollbackFor)은 무시
- private 메서드도 프록시가 오버라이드할 수 없어서 같은 문제
- 해결: **별도 빈으로 분리**(권장)

## 롤백 규칙

| 예외 | 기본 동작 | 이유 |
|---|---|---|
| RuntimeException, Error | 롤백 | 예상 못 한 오류 → 데이터 상태를 믿을 수 없음 |
| Checked 예외 | **커밋** | 예상 가능·복구 가능한 비즈니스 예외로 봄 |

`@Transactional(rollbackFor = Exception.class)`로 바꿀 수 있어요.

## 전파 속성

이미 트랜잭션이 있을 때 트랜잭션 메서드가 또 호출되면 어떻게 할지 정하는 규칙이에요.

| 속성 | 있을 때 | 없을 때 |
|---|---|---|
| **REQUIRED** (기본) | 참여 | 생성 |
| **REQUIRES_NEW** | 보류하고 새로 생성(새 커넥션) | 생성 |
| SUPPORTS | 참여 | 없이 실행 |
| MANDATORY | 참여 | 예외 |
| NOT_SUPPORTED | 보류하고 없이 실행 | 없이 실행 |
| NEVER | 예외 | 없이 실행 |
| NESTED | 세이브포인트로 중첩 | 생성 |

- REQUIRES_NEW는 감사 로그처럼 본 작업 성패와 무관하게 남겨야 할 때 써요.
- 주의: 안쪽 예외를 바깥에서 안 잡으면 바깥도 롤백 / 요청 하나가 커넥션 2개를 잡아서 커넥션 풀 데드락 위험

## rollback-only

- **물리 트랜잭션**: 실제 커넥션 하나의 트랜잭션. 커밋/롤백은 여기서만 일어나요.
- **논리 트랜잭션**: `@Transactional` 메서드 하나하나. REQUIRED로 참여하면 물리 트랜잭션 하나를 공유해요.

참여자(안쪽)에서 예외가 나면 직접 롤백할 권한이 없어서 공유 트랜잭션 상태에 **rollback-only** 표시만 해요. 바깥에서 예외를 catch해도 표시는 남아서, 커밋 시점에 롤백되고 `UnexpectedRollbackException`이 터져요.

> 모든 논리 트랜잭션이 커밋돼야 물리 트랜잭션이 커밋된다.

해결: 안쪽을 REQUIRES_NEW로 / 안쪽에서 예외를 직접 처리 / `noRollbackFor`

## readOnly = true

- JPA: flush 모드 MANUAL → 스냅샷·변경 감지·flush 생략 → 메모리·CPU 절약
- JDBC: `setReadOnly(true)` → DB 읽기 전용 최적화
- 레플리카(읽기 DB) 라우팅 기준으로 활용
- 엔티티를 수정하면 에러 없이 **조용히 반영 안 됨**, 직접 쓰기 쿼리는 DB에 따라 에러

## 면접용 한 줄

"@Transactional은 AOP 프록시가 호출을 가로채 트랜잭션 매니저로 커넥션의 auto-commit을 끄고, ThreadLocal로 같은 커넥션을 공유하다가 RuntimeException이면 롤백, 아니면 커밋합니다. 프록시 기반이라 내부 호출에는 적용되지 않습니다."
