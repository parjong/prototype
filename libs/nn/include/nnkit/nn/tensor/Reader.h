#ifndef __NNKIT_NN_TENSOR_READER_H__
#define __NNKIT_NN_TENSOR_READER_H__

#include "nnkit/nn/tensor/Index.h"

namespace nnkit
{
namespace nn
{
namespace tensor
{

template<typename T> struct Reader
{
  virtual ~Reader() = default;

  virtual T at(const Index &) const = 0;
};

} // namespace tensor
} // namespace nn
} // namespace nnkit

#endif // __NNKIT_NN_TENSOR_READER_H__
