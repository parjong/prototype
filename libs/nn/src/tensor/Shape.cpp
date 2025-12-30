#include "nnkit/nn/tensor/Shape.h"

namespace nnkit
{
namespace nn
{
namespace tensor
{

uint32_t Shape::rank(void) const
{
  return _dims.size();
}

Shape &Shape::resize(uint32_t size)
{
  _dims.resize(size);
}

uint64_t &Shape::dim(uint32_t axis)
{
  return _dims.at(axis);
}

const uint64_t &Shape::dim(uint32_t axis) const
{
  return _dims.at(axis);
}

} // namespace tensor
} // namespace nn
} // namespace nnkit


