# modules-visibility

C++20 모듈로 `.h` / `.cpp` 분리 없이 가시성(visibility)을 제어하는 예제.

- `counter.cppm`: 주 인터페이스. `export`한 `Counter`만 밖에서 보인다. `internal_helper`는 export하지 않아 이름 조회가 안 된다.
- `counter-detail.cppm`: 구현 파티션(`module counter:detail;`). `export`가 없으므로 모듈 내부에서만 import할 수 있고 외부에서는 보이지 않는다.
- `main.cpp`: `import counter;`만으로 사용. 주석 처리된 호출 3개는 컴파일 에러가 나야 한다.

## 빌드

```sh
cmake -S . -B build -G Ninja
cmake --build build
./build/app
```

CMake 3.28+, Ninja, GCC 14+ / Clang 16+.
