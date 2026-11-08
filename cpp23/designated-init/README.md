# designated-init

C++20 designated initializer와 필드 누락을 막는 방법.

- 선언 순서대로만 쓸 수 있고, 지정자와 위치 기반 초기화는 섞을 수 없다 (둘 다 컴파일 에러).
- 생략한 필드는 기본 멤버 초기화자로, 없으면 값 초기화(0)된다.

## 필드 누락 막기

| 방법 | 동작 |
| --- | --- |
| `-Werror=missing-field-initializers` (`-Wextra` 포함) | 기본 멤버 초기화자가 **없는** 필드를 누락하면 에러. 기본값이 있는 필드는 누락해도 경고하지 않음 |
| `Required<T>` 래퍼 (기본 생성자 `= delete`) | 해당 필드를 누락하면 항상 컴파일 에러. 경고 옵션에 의존하지 않음. 선택 필드는 그냥 기본값을 둔 일반 타입으로 |

## 빌드

```sh
g++ -std=c++23 -Wall -Wextra -o main main.cpp && ./main      # Point{.x = 1}에서 경고
g++ -std=c++23 -Werror=missing-field-initializers main.cpp    # 에러로 승격
```

필요 버전: GCC 8+.
