// C++23 `import std;` 예제.
// #include <vector> <string> <print> ... 를 나열하는 대신 한 줄로 끝난다.

import std;
import geometry;

int main() {
  std::vector<geometry::Point> path{{0, 0}, {3, 4}, {3, 10}};

  double total = 0;
  for (std::size_t i = 1; i < path.size(); ++i) {
    total += geometry::distance(path[i - 1], path[i]);
  }

  std::println("points: {}", path.size());
  std::println("path length: {}", total);
}
