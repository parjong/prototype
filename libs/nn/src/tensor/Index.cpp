#include "nnkit/nn/tensor/Index.h"

namespace nnkit
{
namespace nn
{
namespace tensor
{

uint32_t Index::rank(void) const
{
  return _indices.size();
}

Index &Index::resize(uint32_t size)
{
  _indices.resize(size);
  return (*this);
}

uint64_t &Index::at(uint32_t axis)
{
  return _indices.at(axis);
}

const uint64_t &Index::at(uint32_t axis) const
{
  return _indices.at(axis);
}

} // namespace tensor
} // namespace nn
} // namespace nnkit
