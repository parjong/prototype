#include <gtest/gtest.h>

#include "nnkit/nn/tensor/Index.h"

TEST(TensorIndexTest, resize)
{
  nnkit::nn::tensor::Index index;

  ASSERT_EQ(index.rank(), 0);
  index.resize(4);
  ASSERT_EQ(index.rank(), 4);
}
