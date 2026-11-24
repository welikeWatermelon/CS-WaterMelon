# 🗺️ 과목별 로드맵

순서대로 안 해도 괜찮아요. 그날 끌리는 과목에서 다음 주제를 고르면 돼요.
공부한 주제는 `[x]`로 체크하고, README 진도표에 자동으로 반영돼요.

> 비중: ★★★ 실무·면접에서 가장 자주 나옴 / ★★ 기본기 / ★ 알아두면 좋음

---

## 💻 OS (+ 컴퓨터구조)  ★★

### 컴퓨터구조 (백엔드에 필요한 만큼)
- [ ] CPU, 메모리, 디스크 — 메모리 계층과 접근 속도 차이
- [ ] CPU 캐시와 지역성(locality)
- [ ] 인터럽트와 시스템 콜
- [ ] 32bit / 64bit, 바이트 오더(엔디안)

### 프로세스와 스레드
- [ ] 프로세스 vs 스레드, 메모리 구조(Code/Data/Heap/Stack)
- [ ] PCB와 컨텍스트 스위칭
- [ ] 멀티프로세스 vs 멀티스레드
- [ ] 사용자 수준 스레드 vs 커널 수준 스레드
- [ ] CPU 스케줄링 (FCFS, SJF, RR, MLFQ)

### 동기화와 교착상태
- [ ] 경쟁 조건, 임계 영역
- [ ] 뮤텍스 vs 세마포어 vs 모니터
- [ ] 데드락 4조건과 예방·회피(은행원 알고리즘)·탐지
- [ ] 스핀락, CAS

### 메모리
- [ ] 가상 메모리, 페이징, 페이지 테이블, TLB
- [ ] 세그멘테이션, 단편화
- [ ] 페이지 교체 알고리즘 (FIFO, LRU, LFU)
- [ ] 스래싱

### I/O와 파일
- [ ] 블로킹/논블로킹, 동기/비동기
- [ ] I/O 멀티플렉싱 (select, poll, epoll)
- [ ] 파일 디스크립터, inode
- [ ] 페이지 캐시, mmap, zero-copy

---

## 🌐 Network  ★★

### 기본 모델
- [ ] OSI 7계층 vs TCP/IP 4계층
- [ ] 브라우저에 URL 입력 후 일어나는 일
- [ ] IP, 서브넷, NAT, 공인/사설 IP

### 전송 계층
- [ ] TCP vs UDP
- [ ] 3-way / 4-way handshake, TIME_WAIT
- [ ] 흐름 제어, 혼잡 제어
- [ ] 포트, 소켓, keep-alive

### HTTP
- [ ] HTTP 메서드, 상태 코드, 멱등성
- [ ] HTTP/1.1 vs HTTP/2 vs HTTP/3
- [ ] 쿠키, 세션, 토큰(JWT)
- [ ] CORS, Same-Origin Policy
- [ ] REST 설계 원칙
- [ ] 캐시 헤더 (Cache-Control, ETag)

### 보안·인프라 연결
- [ ] HTTPS, TLS handshake, 대칭/비대칭키
- [ ] DNS 동작 과정
- [ ] L4 vs L7 로드밸런서
- [ ] 프록시, 리버스 프록시, CDN
- [ ] WebSocket, SSE, 폴링

---

## 🗄️ DB  ★★★

### 인덱스
- [ ] 인덱스 동작 원리, B-Tree vs B+Tree
- [x] 클러스터드 vs 논클러스터드 인덱스
- [ ] 복합 인덱스와 컬럼 순서
- [ ] 커버링 인덱스
- [ ] 인덱스를 못 타는 경우
- [ ] 실행계획 읽기 (EXPLAIN)

### 트랜잭션
- [ ] ACID
- [ ] 격리 수준 4단계와 이상 현상 (Dirty/Non-repeatable/Phantom Read)
- [ ] MVCC, Undo 로그
- [ ] Redo 로그, WAL

### 락과 동시성
- [ ] 공유락 vs 배타락
- [ ] 레코드락, 갭락, 넥스트키락
- [ ] 낙관적 락 vs 비관적 락
- [ ] DB 데드락

### 설계와 쿼리
- [ ] 정규화 1~3NF, BCNF, 반정규화
- [ ] 조인 종류와 조인 알고리즘 (NL, Hash, Merge)
- [ ] 서브쿼리 vs 조인
- [ ] 페이징 — offset vs 커서(no-offset)

### 확장과 운영
- [ ] 레플리케이션, 읽기/쓰기 분리
- [ ] 샤딩, 파티셔닝
- [ ] 커넥션 풀
- [ ] RDB vs NoSQL, Redis 자료구조

---

## ☕ Java  ★★★

### JVM
- [ ] JVM 구조 (클래스로더, Runtime Data Area, 실행 엔진)
- [ ] 힙 구조와 GC 동작 (Young/Old, Minor/Major GC)
- [ ] GC 종류 (Serial, Parallel, G1, ZGC)
- [ ] JIT 컴파일러

### 언어 기본
- [ ] equals / hashCode 계약
- [ ] String 불변성, String Pool
- [ ] 오버로딩 vs 오버라이딩, 추상클래스 vs 인터페이스
- [ ] Checked vs Unchecked 예외
- [ ] 제네릭과 타입 소거
- [ ] 리플렉션

### 컬렉션
- [ ] ArrayList vs LinkedList
- [ ] HashMap 내부 구조 (버킷, 해시 충돌, 트리화)
- [ ] TreeMap, LinkedHashMap
- [ ] ConcurrentHashMap

### 동시성
- [ ] synchronized, volatile, 메모리 가시성
- [ ] Atomic 클래스와 CAS
- [ ] ExecutorService, 스레드 풀
- [ ] CompletableFuture
- [ ] Virtual Thread (Java 21)

### 모던 Java
- [ ] 람다, 함수형 인터페이스, Stream
- [ ] Optional 올바르게 쓰기
- [ ] record, sealed class, 패턴 매칭

---

## 🌱 Spring  ★★★

### 핵심 원리
- [ ] IoC / DI, 빈 생명주기
- [ ] 빈 스코프 (singleton, prototype, request)
- [ ] AOP, 프록시 (JDK 동적 프록시 vs CGLIB)
- [ ] 스프링 부트 자동 설정 원리

### 웹 MVC
- [ ] DispatcherServlet 요청 처리 흐름
- [ ] Filter vs Interceptor vs AOP
- [ ] ArgumentResolver, MessageConverter
- [ ] 예외 처리 (@ControllerAdvice)
- [ ] 톰캣 스레드 모델

### 트랜잭션
- [x] @Transactional 동작 원리
- [x] 전파 속성 (REQUIRED, REQUIRES_NEW, NESTED)
- [x] 같은 클래스 내부 호출 시 트랜잭션이 안 먹는 이유
- [x] readOnly, 롤백 규칙

### 데이터 접근
- [ ] JPA 영속성 컨텍스트, 1차 캐시, 변경 감지
- [ ] 지연 로딩과 N+1 문제, fetch join
- [ ] JPA vs MyBatis
- [ ] OSIV

### 기타
- [ ] Spring Security 필터 체인, 인증 흐름
- [ ] @Async, @Scheduled
- [ ] Spring Cache 추상화
- [ ] 테스트 (단위 / 슬라이스 / 통합)

---

## ☁️ Infra / Cloud  ★★

### AWS
- [ ] VPC, 서브넷, 보안그룹, NACL
- [ ] EC2, Auto Scaling, ELB(ALB/NLB)
- [ ] RDS, S3, CloudFront
- [ ] IAM 역할과 정책
- [ ] ECS / EKS 개요, Lambda

### 컨테이너와 배포
- [ ] 컨테이너 vs VM, Docker 이미지 레이어
- [ ] Docker Compose
- [ ] Kubernetes 기본 오브젝트 (Pod, Deployment, Service)
- [ ] CI/CD 파이프라인
- [ ] 무중단 배포 (롤링, 블루그린, 카나리)

### 운영
- [ ] 로그 수집, 모니터링 (Prometheus, Grafana)
- [ ] 장애 대응, 헬스체크
- [ ] 리눅스 기본 명령어 (top, netstat/ss, lsof)

---

## 🏗️ 시스템 설계  ★★★

### 캐시
- [ ] 캐시 전략 (Cache-Aside, Write-Through, Write-Back)
- [ ] 캐시 무효화, TTL
- [ ] 캐시 스탬피드, 핫키 문제
- [ ] 로컬 캐시 vs 분산 캐시

### 비동기와 메시징
- [ ] 메시지 큐 (Kafka vs RabbitMQ)
- [ ] 전달 보장 (at-most / at-least / exactly-once)
- [ ] 이벤트 기반 아키텍처, Outbox 패턴

### 분산 시스템
- [ ] 수평 확장 vs 수직 확장
- [ ] CAP, PACELC
- [ ] 분산 락 (Redis, DB)
- [ ] 분산 트랜잭션, SAGA
- [ ] 멱등성 키 설계

### 안정성
- [ ] Rate Limiting (토큰 버킷 등)
- [ ] Circuit Breaker, Retry, Timeout
- [ ] 대용량 트래픽 대응 (선착순, 재고 차감)

### 설계 연습
- [ ] URL 단축기
- [ ] 상품 전시 / 기획전 페이지
- [ ] 실시간 랭킹
- [ ] 알림 시스템
- [ ] 쿠폰 발급 시스템
