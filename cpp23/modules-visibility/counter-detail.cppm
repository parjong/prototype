// 구현 파티션(implementation partition): 모듈 `counter`의 내부 구현 조각.
// `export`가 없는 파티션은 같은 모듈 안에서만 import할 수 있고, 외부에서는 보이지 않는다.
// (인터페이스 파티션 `export module counter:x;`은 주 인터페이스가 `export import`해야 한다.)
module;
#include <string>
module counter:detail;

std::string pad(std::string s, std::size_t width) {
  if (s.size() < width) s.insert(0, width - s.size(), '0');
  return s;
}
