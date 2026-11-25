# ☕ Java — Q&A 모음

출퇴근 때 푼 문제를 날짜순으로 쌓아요. 면접 직전에 이 파일만 훑어봐도 되게끔 모범답안은 짧게 정리해요.

<!-- 새 문제는 아래에 추가 -->

### 2026-11-26 — JVM 구조
**Q. 소스가 실행되기까지 JVM은 어떤 과정을 거치나요?**
- javac로 바이트코드(.class) 생성 → 클래스 로더가 적재 → Runtime Data Area(Heap/Stack/Method Area) → 실행 엔진(인터프리터+JIT, GC)이 실행

### 2026-11-26 — Stack과 Heap
**Q. `Person p = new Person()`에서 p와 객체는 어디에 저장되나요?**
- 참조 변수 p는 Stack, 객체는 Heap. 기본형 지역변수는 값이 Stack에 저장
- 메서드 종료로 p가 사라지면 가리키는 곳이 없는 객체는 GC 대상

### 2026-11-26 — GC 판단 기준, Young/Old
**Q. GC는 안 쓰는 객체를 어떻게 판단하고, 힙을 왜 Young/Old로 나누나요?**
- GC Root(Stack 지역변수, static 변수, 스레드)에서 도달 불가능하면 회수 (static도 Root라 누수 원인이 될 수 있음)
- 대부분 객체는 금방 죽으니 Young에서 자주(Minor GC), age가 임계값을 넘은 객체는 Old로 승격해 드물게(Major GC)

### 2026-11-26 — Stop-The-World
**Q. Stop-The-World란? 왜 문제인가요?**
- GC 중 애플리케이션 스레드를 모두 멈추는 것. 요청 처리가 멈춰 지연·타임아웃 발생
- Serial/Parallel → G1(Region 분할) → ZGC(동시 처리)로 STW를 줄이는 방향으로 발전

### 2026-11-26 — GC 의심 시 확인 순서
**Q. 서버가 가끔 몇 초씩 멈추는데 GC가 원인인 것 같다면?**
- GC 로그(`-Xlog:gc*`)에서 pause 시각·Full GC 빈도·청소 후 Old 사용량 확인, jstat·모니터링, 누수면 힙 덤프(MAT)
- 대응: 힙 크기 조정, GC 변경, 누수 코드 수정

### 2026-11-26 — equals와 hashCode
**Q. `==`와 equals 차이, equals가 true면 hashCode가 같아야 하는 이유는?**
- `==` 참조 비교, equals는 오버라이드해야 값 비교
- HashMap은 hashCode로 버킷을 찾고 equals로 확인 → 계약이 깨지면 같은 값이 다른 버킷에 들어가 조회 실패·중복 발생. 같은 필드로 함께 오버라이드

### 2026-11-26 — String Pool
**Q. `"abc" == "abc"`, `"abc" == new String("abc")`는?**
- true, false. 리터럴은 String Pool 공유, new는 Heap에 새 객체. 값 비교는 equals, intern()으로 Pool 객체 획득

### 2026-11-26 — String 불변성
**Q. String은 왜 불변인가요?**
- Pool 공유(메모리 절약)가 가능하고, HashMap 키로 안전(해시 불변·캐싱), 스레드 안전, 보안(검증 후 변경 방지)
