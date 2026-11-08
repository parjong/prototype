// C++20 동시성 추가분 예제: jthread, stop_token, latch, barrier, semaphore, atomic wait.
// C++17에서는 std::thread + mutex + condition_variable로 직접 만들어야 했다.
// 출력 순서가 실행마다 달라지지 않도록, 스레드 안에서는 출력하지 않고 join 이후 결과만 출력한다.

#include <atomic>
#include <barrier>
#include <chrono>
#include <latch>
#include <print>
#include <semaphore>
#include <stop_token>
#include <thread>
#include <vector>

using namespace std::chrono_literals;

// 1) jthread: 소멸자에서 자동 join + 협력적 취소(stop_token)
void jthread_demo() {
  std::atomic<int> ticks{0};
  {
    std::jthread worker([&](std::stop_token st) {
      while (!st.stop_requested()) {
        ++ticks;
        std::this_thread::sleep_for(1ms);
      }
    });
    std::this_thread::sleep_for(20ms);
  }  // ~jthread: request_stop() 후 join() (std::thread는 join을 잊으면 terminate)
  std::println("jthread: worker stopped, ticked: {}", ticks.load() > 0);

  // 취소 시점에 콜백 실행
  std::stop_source source;
  bool called = false;
  std::stop_callback cb(source.get_token(), [&] { called = true; });
  source.request_stop();
  std::println("stop_callback called: {}", called);
}

// 2) latch: 1회용 카운트다운 (N개 작업이 끝날 때까지 대기)
void latch_demo() {
  constexpr int n = 4;
  std::latch done(n);
  std::vector<int> results(n);
  std::vector<std::jthread> threads;
  for (int i = 0; i < n; ++i) {
    threads.emplace_back([&, i] {
      results[i] = i * i;
      done.count_down();
    });
  }
  done.wait();
  int sum = 0;
  for (int r : results) sum += r;
  std::println("latch: sum of squares = {}", sum);
}

// 3) barrier: 반복 가능한 동기화 지점 (+ 단계 종료 시 completion 함수)
void barrier_demo() {
  constexpr int n = 3;
  int phases = 0;  // completion 함수는 한 스레드에서만 실행되므로 race 없음
  std::barrier sync(n, [&]() noexcept { ++phases; });
  {
    std::vector<std::jthread> threads;
    for (int i = 0; i < n; ++i) {
      threads.emplace_back([&] {
        for (int round = 0; round < 3; ++round) sync.arrive_and_wait();
      });
    }
  }
  std::println("barrier: completed phases = {}", phases);
}

// 4) counting_semaphore: 동시에 N개까지만 허용
void semaphore_demo() {
  std::counting_semaphore<2> slots(2);
  std::atomic<int> running{0}, max_running{0};
  {
    std::vector<std::jthread> threads;
    for (int i = 0; i < 6; ++i) {
      threads.emplace_back([&] {
        slots.acquire();
        int now = ++running;
        int prev = max_running.load();
        while (prev < now && !max_running.compare_exchange_weak(prev, now)) {}
        std::this_thread::sleep_for(5ms);
        --running;
        slots.release();
      });
    }
  }
  std::println("semaphore: max concurrent <= 2: {}", max_running.load() <= 2);
}

// 5) atomic wait/notify: condition_variable 없이 값 변화를 기다림
void atomic_wait_demo() {
  std::atomic<bool> ready{false};
  bool seen = false;
  std::jthread waiter([&] {
    ready.wait(false);  // 값이 false가 아닐 때까지 블록
    seen = true;
  });
  std::this_thread::sleep_for(5ms);
  ready = true;
  ready.notify_one();
  waiter.join();
  std::println("atomic wait: woke up = {}", seen);
}

int main() {
  jthread_demo();
  latch_demo();
  barrier_demo();
  semaphore_demo();
  atomic_wait_demo();
}
