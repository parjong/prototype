// C++23 std::generator (코루틴 기반 지연 시퀀스) 예제.
// C++20에는 코루틴 언어 기능만 있고 generator 타입이 없어서
// promise_type을 직접 쓰거나 서드파티(cppcoro 등)를 써야 했다.

#include <generator>
#include <iostream>
#include <memory>
#include <ranges>
#include <string_view>

// 1) 무한 시퀀스 - 호출자가 필요한 만큼만 꺼낸다 ---------------------------

std::generator<int> fibonacci() {
  int a = 0, b = 1;
  while (true) {
    co_yield a;
    int next = a + b;
    a = b;
    b = next;
  }
}

// 2) 다른 range와 파이프라인으로 결합 (generator는 input_range이자 view) -----

std::generator<int> naturals() {
  for (int n = 1;; ++n) co_yield n;
}

// 3) 재귀 - elements_of로 하위 generator를 위임 -------------------------------

struct Node {
  int value;
  std::unique_ptr<Node> left, right;
  explicit Node(int v) : value(v) {}
};

void insert(std::unique_ptr<Node>& root, int v) {
  if (!root) {
    root = std::make_unique<Node>(v);
  } else if (v < root->value) {
    insert(root->left, v);
  } else {
    insert(root->right, v);
  }
}

std::generator<int> inorder(const Node* n) {
  if (!n) co_return;
  co_yield std::ranges::elements_of(inorder(n->left.get()));
  co_yield n->value;
  co_yield std::ranges::elements_of(inorder(n->right.get()));
}

// 4) 입력을 지연 파싱 - 줄 단위로 string_view를 yield ------------------------
//    인자를 값으로 받는다. (참조 인자는 코루틴이 중단된 동안 dangling이 될 수 있음)

std::generator<std::string_view> lines(std::string_view text) {
  while (!text.empty()) {
    auto pos = text.find('\n');
    co_yield text.substr(0, pos);
    if (pos == std::string_view::npos) co_return;
    text.remove_prefix(pos + 1);
  }
}

int main() {
  std::cout << "fibonacci:";
  for (int x : fibonacci() | std::views::take(10)) std::cout << ' ' << x;
  std::cout << '\n';

  std::cout << "squares of odd naturals:";
  for (int x : naturals() | std::views::filter([](int n) { return n % 2 == 1; }) |
                   std::views::transform([](int n) { return n * n; }) |
                   std::views::take(5)) {
    std::cout << ' ' << x;
  }
  std::cout << '\n';

  std::unique_ptr<Node> root;
  for (int v : {5, 2, 8, 1, 9, 3}) insert(root, v);
  std::cout << "inorder:";
  for (int x : inorder(root.get())) std::cout << ' ' << x;
  std::cout << '\n';

  for (std::string_view line : lines("first\nsecond\nthird")) {
    std::cout << "line: " << line << '\n';
  }
}
