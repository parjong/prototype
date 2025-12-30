#ifndef __NNKIT_NN_TENSOR_INDEX_H__
#define __NNKIT_NN_TENSOR_INDEX_H__

#include <vector>
#include <cstdint>

namespace nnkit
{
namespace nn
{
namespace tensor
{

class Index
{
public:
  uint32_t rank(void) const;

public:
  Index &resize(uint32_t size);

public:
  uint64_t &at(uint32_t axis);
  const uint64_t &at(uint32_t axis) const;

private:
  std::vector<uint64_t> _indices;
};

} // namespace tensor
} // namespace nn
} // namespace nnkit

#endif // __NNKIT_NN_TENSOR_INDEX_H__
