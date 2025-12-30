#include <gtest/gtest.h>

#include "nnkit/nn/tensor/IndexIterator.h"

#include <array>
#include <algorithm>

using namespace nnkit::nn;

TEST(TensorIndexIteratorTest, iterate)
{
  tensor::Shape shape;

  shape.resize(3);
  shape.dim(0) = 2;
  shape.dim(1) = 4;
  shape.dim(2) = 3;

  std::array<int, 2 * 4 * 3> arr;

  arr.fill(0);

  tensor::iterate(shape) << [&arr, &shape] (const tensor::Index &index)
  {
    uint64_t offset = index.at(0);

    for (uint32_t axis = 1; axis < index.rank(); ++axis)
    {
      offset *= shape.dim(axis);
      offset += index.at(axis);
    }

    arr[offset] += 1;
  };

  ASSERT_TRUE(std::all_of(arr.begin(), arr.end(), [] (int n) { return n == 1; }));
}
