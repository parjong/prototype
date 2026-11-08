#include <iostream>
import counter;

int main() {
  Counter c;
  c.inc();
  c.inc();
  std::cout << c.label() << '\n';   // count=002

  // 아래는 모두 컴파일 에러 (확인하려면 주석을 풀어 볼 것)
  // pad("7", 3);          // :detail 파티션은 export되지 않음
  // internal_helper();    // export되지 않은 이름
  // c.n_ = 5;             // private 멤버
}
