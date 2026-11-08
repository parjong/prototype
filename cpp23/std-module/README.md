# std-module

C++23 `import std;`와 직접 만든 모듈(`export module geometry;`) 예제.

- `geometry.cppm`: 모듈 인터페이스 단위. 헤더 + `.cpp` 쌍을 대체한다. `export`하지 않은 `detail::square`는 밖에서 안 보인다.
- `main.cpp`: `import std;` 한 줄로 `std::vector`, `std::println`, `std::sqrt` 등을 모두 사용.

C++17의 `#include` 방식과 달리 매크로가 새어 들어오지 않고, 헤더를 반복해서 파싱하지 않는다.

## 빌드

모듈 빌드는 빌드 시스템 지원이 필요하다. CMake + Ninja를 사용한다.

```sh
cmake -S . -B build -G Ninja
cmake --build build
./build/app
```

요구 사항:

- CMake 3.30+ (모듈 지원), Ninja 1.11+
- `import std;`를 지원하는 컴파일러: GCC 15+ 또는 Clang 18+ (libc++)

> CMake 버전에 따라 `import std` 활성화 방법(실험 기능 UUID)이 다르다.
> `CMakeLists.txt`의 주석을 참고해서 사용 중인 버전에 맞게 조정할 것.
