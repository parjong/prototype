// C++23에서 추가된 ranges 기능 예제.
// C++17에서는 손으로 쓰던 루프를 파이프라인으로 표현한다.

#include <algorithm>
#include <functional>
#include <iostream>
#include <ranges>
#include <string>
#include <string_view>
#include <vector>

namespace rv = std::views;

template <std::ranges::input_range R>
void show(std::string_view label, R&& r) {
  std::cout << label << ": [";
  bool first = true;
  for (auto&& x : r) {
    if (!first) std::cout << ", ";
    first = false;
    std::cout << x;
  }
  std::cout << "]\n";
}

int main() {
  const std::vector<std::string> names{"alice", "bob", "carol"};
  const std::vector<int> scores{90, 72, 85};

  // C++20: filter / transform / take 파이프라인 (지연 평가)
  show("squares of evens",
       rv::iota(1, 20) | rv::filter([](int n) { return n % 2 == 0; }) |
           rv::transform([](int n) { return n * n; }) | rv::take(5));

  // C++23: ranges::to - 파이프라인 결과를 컨테이너로 바로 변환
  auto evens = rv::iota(1, 11) | rv::filter([](int n) { return n % 2 == 0; }) |
               std::ranges::to<std::vector>();
  show("evens (vector)", evens);

  // C++23: views::zip - 여러 range를 나란히 순회
  for (auto [name, score] : rv::zip(names, scores)) {
    std::cout << name << " -> " << score << '\n';
  }

  // C++23: views::enumerate - 인덱스와 함께 순회 (for (size_t i...) 대체)
  for (auto [i, name] : rv::enumerate(names)) {
    std::cout << i << ": " << name << '\n';
  }

  // C++23: views::chunk - 고정 크기로 나누기
  const std::vector<int> v{1, 2, 3, 4, 5, 6, 7};
  for (auto c : v | rv::chunk(3)) show("chunk", c);

  // C++23: views::slide - 크기 N의 이동 윈도우
  for (auto w : v | rv::slide(3)) show("window", w);

  // C++23: views::stride - N칸씩 건너뛰기
  show("stride 3", v | rv::stride(3));

  // C++23: views::chunk_by - 인접 원소 조건으로 묶기 (여기서는 비감소 구간)
  const std::vector<int> runs{1, 2, 2, 1, 3, 4, 0};
  for (auto c : runs | rv::chunk_by(std::ranges::less_equal{})) show("run", c);

  // C++23: views::join_with - 구분자를 넣어 이어 붙이기
  auto joined = names | rv::join_with(std::string_view(", ")) |
                std::ranges::to<std::string>();
  std::cout << "joined: " << joined << '\n';

  // C++23: views::cartesian_product - 중첩 for 대체
  for (auto [x, y] : rv::cartesian_product(rv::iota(0, 2), rv::iota(0, 3))) {
    std::cout << '(' << x << ',' << y << ") ";
  }
  std::cout << '\n';

  // C++23: ranges::fold_left - std::accumulate의 range 버전
  std::cout << "sum = " << std::ranges::fold_left(v, 0, std::plus<>{}) << '\n';
}
