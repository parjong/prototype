#include "hello.h"

#include <iostream>

namespace
{

class X final
{
private:
  X() = default;

public:
  static X make(void) { return X{}; }
};

} // namespace

int main(int argc, char **argv)
{
  std::cout << hello() << std::endl;
  std::make_shared<X>();
  return 0;
}
