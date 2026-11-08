# concurrency

C++20 동시성 추가분 예제.

| 기능 | 대체하는 C++17 방식 |
| --- | --- |
| `std::jthread`, `std::stop_token`, `stop_callback` | `std::thread` + 수동 join + 취소용 `atomic<bool>` |
| `std::latch` | `mutex` + `condition_variable` + 카운터 |
| `std::barrier` | 직접 만든 재사용 가능 barrier |
| `std::counting_semaphore` | `mutex` + `condition_variable` |
| `atomic::wait` / `notify_one` | `condition_variable` 또는 스핀 |

스레드 안에서는 출력하지 않고 join 이후 결과만 출력해서 실행마다 출력이 같다.

## 빌드

```sh
g++ -std=c++23 -pthread -Wall -Wextra -o main main.cpp && ./main
```

필요 버전: GCC 14+ (`std::println`; 동시성 기능 자체는 GCC 11+).
