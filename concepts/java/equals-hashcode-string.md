# equals / hashCode와 String

## 한 줄 요약

`equals()`가 true인 객체는 `hashCode()`도 같아야 해요. HashMap이 **hashCode로 칸을 찾고, equals로 확인**하기 때문이에요.

## == vs equals

- `==`: 참조(주소) 비교
- `equals()`: 오버라이드해야 값 비교. Object 기본 구현은 `==`와 같아요. String, Integer 등은 값 비교로 오버라이드돼 있어요.

## HashMap 저장·조회 과정

**저장 `put(key, value)`**
1. `key.hashCode()` 계산
2. 해시값으로 버킷 배열의 칸 번호 결정 (기본 16칸, 대략 `해시 % 크기`)
3. 그 칸에 (key, value) 저장
4. 이미 다른 키가 있으면(충돌) `equals()`로 같은 키인지 확인. 같으면 value 덮어쓰기, 다르면 연결 리스트로 이어 붙여요 (8개 이상이면 트리화)

**조회 `get(key)`**: 같은 방식으로 칸을 찾고, 칸 안에서 `equals()`로 찾아요.

## 계약이 깨지면

```java
Person a = new Person(1, "kim");
Person b = new Person(1, "kim");   // equals는 true, hashCode는 다름
map.put(a, "값");
map.get(b);   // 다른 칸을 뒤져서 null
```

- Set에 같은 값이 중복으로 들어가기도 해요.
- 역방향(hashCode가 같으면 equals도 같다)은 필수가 아니에요 (해시 충돌).
- 같은 필드로 둘을 **함께** 오버라이드해요. `Objects.hash(id, name)`

## String Pool

```java
String s1 = "abc";
String s2 = "abc";
String s3 = new String("abc");
s1 == s2          // true  (Pool 공유)
s1 == s3          // false (Heap에 새 객체)
s1.equals(s3)     // true
s1 == s3.intern() // true
```

## String이 불변인 이유

- Pool 공유로 메모리를 아낄 수 있어요. 불변이라서 가능해요. 가변이면 한 곳의 변경이 공유하는 곳 전부에 영향을 줘요.
- HashMap 키로 안전해요. 해시값이 안 변하고 캐싱도 가능해요.
- 스레드 안전해요. 동기화 없이 공유할 수 있어요.
- 보안에 좋아요. 검증 후에 값이 바뀌지 않아요.
