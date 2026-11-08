# multidim-subscript

C++23에서 `operator[]`가 여러 인자를 받을 수 있게 된 것(P2128)을 보여주는 예제.

- `Matrix<T>`: `m[r, c]`
- `NdArray<T, Rank>`: 가변 인자 `operator[]` + `requires`로 인자 개수를 Rank와 일치하도록 강제

C++17에서는 `m(r, c)` 또는 `m[r][c]`(행 proxy)로 우회했다.
C++20에서 `a[1, 2]`는 콤마 연산자라 deprecated였고, C++23에서 다차원 인덱스로 의미가 바뀌었다.

참고: 표준 라이브러리의 `std::mdspan`(C++23)도 `operator[]`로 다차원 인덱스를 받는다 (GCC 15+ / libc++ 최신).

## 빌드

```sh
g++ -std=c++23 -Wall -Wextra -o main main.cpp && ./main
```

필요 버전: GCC 12+ (Clang 15+).
