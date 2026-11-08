# ranges

C++23에서 추가된 ranges 기능을 모은 예제.

| 기능 | 대체하는 C++17 코드 |
| --- | --- |
| `std::ranges::to` | 결과를 컨테이너에 옮기는 수동 루프 / `back_inserter` |
| `views::zip` | 인덱스로 두 컨테이너 동시 순회 |
| `views::enumerate` | `for (size_t i = 0; ...)` |
| `views::chunk`, `views::slide`, `views::stride` | 수동 인덱스 계산 |
| `views::chunk_by` | 인접 원소 비교 루프 |
| `views::join_with` | 구분자 붙여 이어 붙이기 |
| `views::cartesian_product` | 중첩 `for` |
| `ranges::fold_left` | `std::accumulate` |

## 빌드

```sh
g++ -std=c++23 -Wall -Wextra -o main main.cpp && ./main
```

필요 버전: GCC 14+ (`ranges::to` 때문).
