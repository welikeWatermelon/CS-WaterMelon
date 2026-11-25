# JVM 구조와 GC

## 한 줄 요약

JVM은 OS 위에서 바이트코드를 대신 실행해 주는 **가상 컴퓨터**예요. 객체는 Heap에 쌓이고, GC가 도달할 수 없는 객체를 회수해요.

## 실행 흐름

1. `javac`가 `.java`를 `.class`(바이트코드)로 컴파일해요.
2. **클래스 로더**가 `.class`를 메모리에 올려요.
3. **Runtime Data Area**에 데이터가 쌓여요.
   - Heap: `new`로 만든 객체 (GC 대상)
   - Stack: 메서드 호출 정보, 지역변수 (스레드마다 1개)
   - Method Area: 클래스 정보, static 변수
4. **실행 엔진**이 실행해요. 인터프리터가 한 줄씩 실행하고, 자주 쓰는 코드는 JIT이 기계어로 바꿔 둬요. GC도 여기에 포함돼요.

## Stack과 Heap

```java
int a = 10;               // a: Stack
Person p = new Person();  // p(참조): Stack → Person 객체: Heap
```

메서드가 끝나면 스택의 p가 사라지고, 아무도 가리키지 않는 객체가 GC 대상이 돼요.

## GC가 쓰레기를 판단하는 기준

- 시간이 아니라 **도달 가능성**이에요. **GC Root**에서 참조를 따라 닿을 수 없는 객체를 회수해요.
- GC Root: Stack의 지역변수, static 변수, 실행 중인 스레드
- static 컬렉션에 계속 담기만 하면 GC가 못 치워서 **메모리 누수**가 나요.

## Young / Old

- 약한 세대 가설: 대부분의 객체는 금방 죽어요.
- 새 객체는 Young(Eden → Survivor)에 두고 자주 청소해요 (Minor GC).
- 객체 헤더의 **age**가 GC에서 살아남을 때마다 올라가고, 임계값(HotSpot 기본 최대 15)을 넘으면 Old로 승격돼요.
- Old는 가끔 크게 청소해요 (Major/Full GC).

## Stop-The-World (STW)

- GC 중 애플리케이션 스레드를 전부 멈추는 것이에요. 멈춘 동안 요청 처리가 안 돼서 지연·타임아웃이 생겨요.

| GC | 특징 |
|---|---|
| Serial | 스레드 1개, 단순, STW 김 |
| Parallel | 여러 스레드, 처리량 중심 (Java 8 기본) |
| G1 | Region으로 나눠 STW를 짧게 쪼갬 (Java 9+ 기본) |
| ZGC | 대부분 동시 처리, STW 아주 짧음 (저지연·대용량 힙) |

## 운영에서 GC가 의심될 때

- GC 로그: `-Xlog:gc*:file=gc.log` (Java 8: `-XX:+PrintGCDetails -Xloggc:gc.log`)
- 볼 것: pause 시간이 응답 지연 시각과 겹치는지, Full GC 빈도, 청소 후 Old 사용량
- 도구: `jstat -gc <pid>`, Prometheus + Grafana, 누수 의심 시 힙 덤프(MAT)
- 대응: 힙 크기(`-Xmx`) 조정, GC 변경, 누수 코드 수정
