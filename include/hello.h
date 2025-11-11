#ifndef __A__
#define __A__

#include <string>

static inline std::string hello(void)
{
  using namespace std::literals::string_literals;
  return "Hello?"s;
}

#endif // __A__
