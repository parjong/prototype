# generator

C++23 `std::generator`로 코루틴 기반 지연 시퀀스를 만드는 예제.

- 무한 시퀀스 (`fibonacci`)와 `views::take` / `filter` / `transform` 파이프라인
- `co_yield std::ranges::elements_of(...)`로 재귀 generator (이진 트리 중위 순회)
- 입력을 지연 파싱하는 generator (`lines`)

주의: generator가 중단된 동안 살아 있어야 하는 인자는 참조가 아니라 값으로 받는다.

## 빌드

```sh
g++ -std=c++23 -Wall -Wextra -o main main.cpp && ./main
```

필요 버전: GCC 14+ (`<generator>`). Clang은 libc++ 쪽 지원 여부를 확인할 것.
