// C++23 std::stacktrace 예제.
// C++17에서는 glibc의 backtrace()나 Boost.Stacktrace 같은 플랫폼/서드파티 도구가 필요했다.

#include <cstdlib>
#include <iostream>
#include <stacktrace>
#include <stdexcept>
#include <string>

// 1) 현재 위치의 스택 트레이스 ------------------------------------------------

void level3() {
  auto st = std::stacktrace::current();
  std::cout << "depth >= 4: " << (st.size() >= 4) << '\n';
  std::cout << "-- full stacktrace --\n" << st << '\n';

  // 개별 프레임: 함수 이름, 파일, 줄 번호
  const auto& top = st[0];
  std::cout << "top frame: " << top.description() << " (" << top.source_file()
            << ':' << top.source_line() << ")\n";
}
void level2() { level3(); }
void level1() { level2(); }

// 2) 예외가 던져진 위치의 스택 트레이스를 예외 객체에 보관 ---------------------
//    (기본 인자로 생성 시점의 trace를 캡처한다)

class TracedError : public std::runtime_error {
 public:
  explicit TracedError(const std::string& msg,
                       std::stacktrace trace = std::stacktrace::current())
      : std::runtime_error(msg), trace_(std::move(trace)) {}
  const std::stacktrace& trace() const { return trace_; }

 private:
  std::stacktrace trace_;
};

void fail() { throw TracedError("something went wrong"); }
void work() { fail(); }

int main() {
  level1();

  try {
    work();
  } catch (const TracedError& e) {
    std::cout << "caught: " << e.what() << "\n" << e.trace() << '\n';
  }
}
