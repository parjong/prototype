// C++17만 쓰던 사람을 위한 C++20/23 신기능 투어.
// 각 섹션은 독립적이며, "C++17에서는 이렇게 했다"를 주석으로 함께 적었다.

#include <bit>
#include <charconv>
#include <compare>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <expected>
#include <functional>
#include <memory>
#include <optional>
#include <print>
#include <source_location>
#include <span>
#include <string>
#include <string_view>
#include <system_error>
#include <utility>
#include <vector>

using namespace std::literals;

// 1) std::expected - 예외 없는 에러 처리 (C++17: optional + out param, 또는 예외)
enum class ParseError { empty, not_a_number };

std::string_view to_string(ParseError e) {
  switch (e) {
    using enum ParseError;  // C++20: enum 이름을 스코프로 가져오기
    case empty: return "empty";
    case not_a_number: return "not a number";
  }
  std::unreachable();  // C++23
}

std::expected<int, ParseError> parse_int(std::string_view s) {
  if (s.empty()) return std::unexpected(ParseError::empty);
  int value{};
  auto [ptr, ec] = std::from_chars(s.data(), s.data() + s.size(), value);
  if (ec != std::errc{} || ptr != s.data() + s.size()) {
    return std::unexpected(ParseError::not_a_number);
  }
  return value;
}

void expected_demo() {
  // transform / and_then으로 연쇄 (C++23 monadic operations)
  auto doubled = parse_int("21").transform([](int v) { return v * 2; });
  std::println("parse_int(\"21\") doubled = {}", doubled.value_or(-1));

  auto bad = parse_int("abc");
  if (!bad) std::println("parse_int(\"abc\") failed: {}", to_string(bad.error()));
}

// 2) std::optional의 monadic operations (C++23)
std::optional<int> first_even(std::span<const int> xs) {
  for (int x : xs) {
    if (x % 2 == 0) return x;
  }
  return std::nullopt;
}

void optional_demo() {
  const std::vector<int> xs{3, 5, 8, 9};
  auto r = first_even(xs)
               .transform([](int v) { return v * 10; })
               .or_else([] { return std::optional<int>{0}; });
  std::println("optional chain = {}", *r);
}

// 3) deducing this (explicit object parameter, C++23)
//    const/non-const 중복 오버로드를 하나로 합친다.
struct Buffer {
  std::vector<int> data;

  decltype(auto) first(this auto& self) { return self.data.front(); }
};

void deducing_this_demo() {
  Buffer b{{1, 2, 3}};
  const Buffer cb{{4, 5, 6}};
  b.first() = 10;  // non-const -> int&
  std::println("b.first() = {}, cb.first() = {}", b.first(), cb.first());

  // 이름 없는 람다도 재귀가 가능하다 (C++17에서는 std::function이 필요했다)
  auto fib = [](this auto self, int n) -> int {
    return n < 2 ? n : self(n - 1) + self(n - 2);
  };
  std::println("fib(10) = {}", fib(10));
}

// 4) static operator() / static lambda (C++23)
struct Square {
  static constexpr int operator()(int x) { return x * x; }
};
static_assert(Square{}(5) == 25);

// 5) if consteval (C++23): 컴파일 타임/런타임 경로 분기
constexpr std::size_t length(const char* s) {
  if consteval {
    std::size_t n = 0;
    while (s[n]) ++n;
    return n;
  } else {
    return std::strlen(s);
  }
}
static_assert(length("abc") == 3);

// 6) 비교 연산자 자동 생성 <=> 와 designated initializer (C++20)
struct Version {
  int major, minor, patch;
  auto operator<=>(const Version&) const = default;
};

void spaceship_demo() {
  Version a{.major = 1, .minor = 2, .patch = 3};
  Version b{.major = 1, .minor = 10, .patch = 0};
  std::println("a < b: {}, a == b: {}", a < b, a == b);
}

// 7) std::span - (포인터, 길이) 쌍 대신 (C++20)
int sum(std::span<const int> xs) {
  int total = 0;
  for (int x : xs) total += x;
  return total;
}

// 8) move-only 호출 가능 객체 (C++23): std::function은 복사 가능해야 했다
void move_only_function_demo() {
  std::move_only_function<int()> f = [p = std::make_unique<int>(42)] { return *p; };
  std::println("move_only_function -> {}", f());
}

// 9) <bit> 유틸리티 (C++20/23)
void bit_demo() {
  std::println("popcount(0xF0F0) = {}", std::popcount(0xF0F0u));
  std::println("byteswap = {:#x}", std::byteswap(std::uint32_t{0x11223344}));
  std::println("bit_cast<uint32_t>(1.0f) = {:#x}",
               std::bit_cast<std::uint32_t>(1.0f));
}

// 10) std::source_location (C++20): __FILE__/__LINE__ 매크로 대체
void log_msg(std::string_view msg,
         std::source_location loc = std::source_location::current()) {
  std::println("[{}:{}] {}", loc.function_name(), loc.line(), msg);
}

int main() {
  expected_demo();
  optional_demo();
  deducing_this_demo();

  std::println("Square::operator() = {}", Square{}(6));
  std::println("length(\"hello\") = {}", length("hello"));

  spaceship_demo();

  const std::vector<int> v{1, 2, 3};
  const int arr[]{4, 5, 6};
  std::println("sum(vector) = {}, sum(array) = {}", sum(v), sum(arr));

  move_only_function_demo();
  bit_demo();

  // C++23: size_t 리터럴 접미사 uz, C++20: string_view의 contains/starts_with
  for (auto i = 0uz; i < 2; ++i) std::println("i = {}", i);
  std::println("contains: {}", "hello world"sv.contains("lo w"));

  log_msg("done");
}
