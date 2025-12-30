#ifndef __NNKIT_NN_TENSOR_INDEX_ITERATOR_H__
#define __NNKIT_NN_TENSOR_INDEX_ITERATOR_H__

#include "nnkit/nn/tensor/Shape.h"
#include "nnkit/nn/tensor/Index.h"

#include <functional>

namespace nnkit
{
namespace nn
{
namespace tensor
{

class IndexIterator
{
public:
  explicit IndexIterator(const Shape &shape);

public:
  void iterate(const std::function<void (const Index &)> &f) const;

private:
  const Shape &_shape;
};

template<typename Callable>
const IndexIterator &operator<<(const IndexIterator &it, Callable cb)
{
  it.iterate(cb);
  return it;
}

IndexIterator iterate(const Shape &shape);

} // namespace tensor
} // namespace nn
} // namespace nnkit

#endif // __NNKIT_NN_TENSOR_INDEX_ITERATOR_H__
