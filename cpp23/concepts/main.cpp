// C++20 concepts 예제 (C++23 환경에서 빌드).
// C++17에서는 SFINAE(enable_if, void_t)로 하던 일을 concept/requires로 표현한다.

#include <concepts>
#include <iostream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>

// 1) requires 표현식으로 직접 만든 concept ---------------------------------

template <typename T>
concept Shape = requires(const T& s) {
  { s.area() } -> std::convertible_to<double>;
  { s.name() } -> std::convertible_to<std::string_view>;
};

struct Circle {
  double r;
  constexpr double area() const { return 3.0 * r * r; }
  constexpr std::string_view name() const { return "circle"; }
};

struct Square {
  double side;
  constexpr double area() const { return side * side; }
  constexpr std::string_view name() const { return "square"; }
};

static_assert(Shape<Circle>);
static_assert(Shape<Square>);
static_assert(!Shape<int>);  // 조건을 만족하지 못하면 컴파일 타임에 false

// 2) 제약이 걸린 함수 템플릿 ---------------------------------------------

template <std::ranges::input_range R>
  requires Shape<std::ranges::range_value_t<R>>
double total_area(const R& shapes) {
  double sum = 0;
  for (const auto& s : shapes) sum += s.area();
  return sum;
}

// 3) 표준 concept + 약식 함수 템플릿(abbreviated function template) ---------

constexpr auto twice(std::integral auto x) { return x * 2; }

constexpr auto half(std::floating_point auto x) { return x / 2; }

// 4) 제약에 의한 오버로드 선택 (subsumption) ------------------------------
//    signed_integral은 integral을 포함(subsume)하므로 더 구체적인 쪽이 선택된다.

template <typename T>
std::string describe(const T&) { return "generic"; }

template <std::integral T>
std::string describe(const T&) { return "integral"; }

template <std::signed_integral T>
std::string describe(const T&) { return "signed integral"; }

// 5) concept 조합: &&, ||, 그리고 직접 만든 concept 재사용 -----------------

template <typename T>
concept Printable = requires(std::ostream& os, const T& v) {
  { os << v } -> std::same_as<std::ostream&>;
};

template <typename T>
concept PrintableRange = std::ranges::input_range<T> &&
                         Printable<std::ranges::range_value_t<T>>;

void print_all(const PrintableRange auto& r) {
  for (const auto& x : r) std::cout << x << ' ';
  std::cout << '\n';
}

int main() {
  const std::vector<Circle> circles{{1.0}, {2.0}};
  const std::vector<Square> squares{{1.0}, {3.0}};
  std::cout << "circles: " << total_area(circles) << '\n';
  std::cout << "squares: " << total_area(squares) << '\n';
  // total_area(std::vector<int>{});  // 에러: 제약 `Shape<int>`를 만족하지 않음

  std::cout << twice(21) << ' ' << half(5.0) << '\n';
  // twice(1.5);  // 에러: double은 std::integral이 아님

  std::cout << describe(1) << '\n';              // signed integral
  std::cout << describe(1u) << '\n';             // integral
  std::cout << describe(1.0) << '\n';            // generic
  std::cout << describe(std::string{}) << '\n';  // generic

  print_all(std::vector<int>{1, 2, 3});
  print_all(std::vector<std::string>{"a", "b"});
}
