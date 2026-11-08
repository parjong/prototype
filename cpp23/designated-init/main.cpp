// C++20 designated initializer 예제와, 필드 누락을 막는 방법.

#include <concepts>
#include <iostream>
#include <string>
#include <utility>

// 1) 기본 사용 ----------------------------------------------------------------
//    - 선언 순서대로만 쓸 수 있다 (C와 달리 순서 바꾸기 불가)
//    - 지정자와 위치 기반 초기화를 섞을 수 없다
//    - 생략한 필드는 기본 멤버 초기화자, 없으면 값 초기화(0)

struct Options {
  std::string host = "localhost";
  int port = 80;
  bool tls = false;
};

// 2) 필드 누락 막기 (a): 컴파일러 경고 ----------------------------------------
//    -Wmissing-field-initializers (-Wextra에 포함)를 -Werror로 승격하면 된다.
//    단, 기본 멤버 초기화자(= "localhost")가 있는 필드는 누락해도 경고하지 않는다.
struct Point {
  int x;
  int y;
};

// 3) 필드 누락 막기 (b): 타입으로 강제 -----------------------------------------
//    기본 생성자가 삭제된 래퍼 타입을 필드로 쓰면, 생략한 필드는 {}로 초기화되어야
//    하는데 그게 불가능하므로 컴파일 에러가 된다. 경고 옵션에 의존하지 않는다.

template <typename T>
struct Required {
  T value;

  Required() = delete;
  template <typename U>
    requires std::convertible_to<U, T>
  constexpr Required(U&& v) : value(std::forward<U>(v)) {}  // NOLINT: implicit
};

struct Config {
  Required<std::string> host;
  Required<int> port;
  bool tls = false;  // 선택 필드
};

int main() {
  Options a{.host = "example.com", .tls = true};  // port는 80
  std::cout << a.host << ':' << a.port << " tls=" << a.tls << '\n';

  // Options b{.port = 8080, .host = "x"};   // 에러: 선언 순서 위반
  // Options c{.host = "x", 8080};           // 에러: 지정자와 위치 기반 혼용

  Point p{.x = 1};  // y는 0으로 값 초기화. -Wextra면 경고 (-Werror로 막을 수 있음)
  std::cout << p.x << ',' << p.y << '\n';

  Config ok{.host = "example.com", .port = 443};
  std::cout << ok.host.value << ':' << ok.port.value << " tls=" << ok.tls << '\n';

  // Config bad{.host = "example.com"};      // 에러: port의 기본 생성자가 삭제됨
}
