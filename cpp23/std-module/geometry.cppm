// 직접 만든 모듈 인터페이스 단위(module interface unit).
// 헤더(.h) + 구현(.cpp) 쌍을 이 파일 하나로 대체한다.
export module geometry;

import std;  // C++23: 표준 라이브러리 전체를 한 번에 import

namespace detail {
// export하지 않은 이름은 모듈 밖에서 보이지 않는다 (헤더의 detail 네임스페이스 관례 불필요).
double square(double x) { return x * x; }
}  // namespace detail

export namespace geometry {

struct Point {
  double x;
  double y;
};

double distance(Point a, Point b) {
  return std::sqrt(detail::square(a.x - b.x) + detail::square(a.y - b.y));
}

}  // namespace geometry
