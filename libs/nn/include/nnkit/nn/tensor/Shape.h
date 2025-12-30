#ifndef __NNKIT_NN_TENSOR_SHAPE_H__
#define __NNKIT_NN_TENSOR_SHAPE_H__

#include <vector>
#include <cstdint>

namespace nnkit
{
namespace nn
{
namespace tensor
{

class Shape
{
public:
  uint32_t rank(void) const;

public:
  Shape &resize(uint32_t size);

public:
  uint64_t &dim(uint32_t axis);
  const uint64_t &dim(uint32_t axis) const;

private:
  std::vector<uint64_t> _dims;
};

} // namespace tensor
} // namespace nn
} // namespace nnkit

#endif // __NNKIT_NN_TENSOR_SHAPE_H__
