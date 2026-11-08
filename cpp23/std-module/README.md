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

- GCC 15+ (또는 Clang 18+ / libc++), Ninja
- CMake 4.0.x 에서 `gcc:15` 도커 이미지로 빌드/실행 확인함

> `import std`는 CMake에서 아직 실험 기능이라, 버전마다 활성화 UUID가 다르다.
> 다른 CMake 버전이면 `CMakeLists.txt`의 UUID를 해당 버전 문서에 맞게 조정할 것.
