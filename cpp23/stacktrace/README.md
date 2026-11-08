# stacktrace

C++23 `std::stacktrace` 예제.

- `std::stacktrace::current()`로 현재 호출 스택을 얻고 출력
- 프레임별 `description()`, `source_file()`, `source_line()`
- 예외 객체 생성 시점의 스택을 보관하는 `TracedError`

C++17에서는 `backtrace()`(glibc), `CaptureStackBackTrace`(Windows), Boost.Stacktrace 등 플랫폼별/서드파티 도구가 필요했다.

## 빌드

심볼 이름과 줄 번호를 보려면 `-g`가 필요하고, GCC 14/15에서는 `-lstdc++exp`를 링크해야 한다.

```sh
g++ -std=c++23 -g -O0 -Wall -Wextra -o main main.cpp -lstdc++exp && ./main
```

필요 버전: GCC 12.1+ (`-lstdcxx-backtrace`), GCC 14+ (`-lstdc++exp`).
