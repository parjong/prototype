// 주 모듈 인터페이스 단위. 헤더(.h) 역할을 하지만 include guard도, 매크로 누수도 없다.
module;
#include <string>
export module counter;

import :detail;  // export 없이 import: 이 모듈 내부에서만 사용

// export한 것만 모듈 밖에서 보인다.
export class Counter {
 public:
  void inc() { ++n_; }
  int value() const { return n_; }
  std::string label() const { return "count=" + pad(std::to_string(n_), 3); }

 private:
  int n_ = 0;
};

// export하지 않은 이름: 모듈 밖에서는 이름 조회 자체가 안 된다 (이름만 가려지는 것이므로
// 헤더의 detail 네임스페이스처럼 관례에 의존하지 않는다).
int internal_helper() { return 42; }

