#include "nnkit/nn/tensor/IndexIterator.h"

using namespace nnkit::nn;

namespace
{

bool valid(const tensor::Index &index, const tensor::Shape &shape)
{
  if (index.rank() != shape.rank())
  {
    return false;
  }

  const auto rank = shape.rank();

  for (uint32_t axis = 0; axis < rank; ++axis)
  {
    if (!(index.at(axis) < shape.dim(axis)))
    {
      return false;
    }
  }

  return true;
}

}

namespace nnkit
{
namespace nn
{
namespace tensor
{

IndexIterator::IndexIterator(const Shape &shape) : _shape(shape)
{
  // DO NOTHING
}

void IndexIterator::iterate(const std::function<void (const Index &)> &f) const
{
  const auto rank = _shape.rank();

  Index index;

  // Initialize index
  index.resize(rank);
  for (uint32_t axis = 0; axis < rank; ++axis)
  {
    index.at(axis) = 0;
  }

  if (!::valid(index, _shape))
  {
    // Nothing to iterate
    return;
  }

  uint32_t cursor = 0;

  while(cursor < rank)
  {
    f(index);

    // Find axis to be updated
    while((cursor < rank) && !(index.at(cursor) + 1 < _shape.dim(cursor)))
    {
      ++cursor;
    }

    // Skip update if cursor is out of valid range
    if(cursor == rank)
    {
      continue;
    }

    // Update index
    index.at(cursor) += 1;

    for (uint32_t axis = 0; axis < cursor; ++axis)
    {
      index.at(axis) = 0;
    }

    // Update cursor
    cursor = 0;
  }
}

IndexIterator iterate(const Shape &shape)
{
  return IndexIterator{shape};
}

} // namespace tensor
} // namespace nn
} // namespace nnkit
