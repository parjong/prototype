# concepts

C++17의 SFINAE(`enable_if`, `void_t`) 대신 `concept` / `requires`로 템플릿 제약을 표현하는 예제.

- `requires` 표현식으로 직접 만든 concept (`Shape`)
- 제약이 걸린 함수 템플릿 / 약식 함수 템플릿 (`std::integral auto`)
- 제약에 의한 오버로드 선택 (subsumption)
- concept 조합 (`PrintableRange`)

## 빌드

```sh
g++ -std=c++23 -Wall -Wextra -o main main.cpp && ./main
```

필요 버전: GCC 12+ (또는 Clang 16+).
