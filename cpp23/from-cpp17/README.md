# from-cpp17

C++17에 익숙한 사람이 알아두면 좋은 C++20/23 신기능 투어. 섹션마다 "C++17에서는 어떻게 했는지"를 주석으로 적었다.

| 기능 | 표준 | 대체하는 C++17 방식 |
| --- | --- | --- |
| `std::expected` | C++23 | 예외, `optional` + out param |
| `optional::transform/and_then/or_else` | C++23 | `if (opt)` 중첩 |
| deducing this (`this auto& self`) | C++23 | const/non-const 오버로드 중복, 재귀 람다에 `std::function` |
| `static operator()` | C++23 | 함수 객체의 불필요한 `this` |
| `if consteval` | C++23 | `std::is_constant_evaluated()` |
| `std::move_only_function` | C++23 | `std::function` (복사 가능만 허용) |
| `std::print` / `println` | C++23 | `printf`, `iostream` |
| `std::unreachable`, `uz` 접미사 | C++23 | 컴파일러 builtin, `size_t{0}` |
| `<=>`, designated initializer | C++20 | 비교 연산자 6개 직접 작성 |
| `using enum` | C++20 | 매번 `Enum::` 접두사 |
| `std::span` | C++20 | `(T*, size_t)` 쌍 |
| `<bit>` (`popcount`, `byteswap`, `bit_cast`) | C++20/23 | 비트 연산 직접 구현, `memcpy` |
| `std::source_location` | C++20 | `__FILE__` / `__LINE__` 매크로 |

concepts, ranges, coroutine generator, 다차원 `operator[]`, `import std;`는 별도 예제로 분리되어 있다.

## 빌드

```sh
g++ -std=c++23 -Wall -Wextra -o main main.cpp && ./main
```

필요 버전: GCC 14+ (`std::print`, deducing this).
