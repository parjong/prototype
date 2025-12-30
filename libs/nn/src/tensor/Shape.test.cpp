#include <gtest/gtest.h>

#include "nnkit/nn/tensor/Shape.h"

TEST(TensorShapeTest, resize)
{
  nnkit::nn::tensor::Shape shape;

  ASSERT_EQ(shape.rank(), 0);
  shape.resize(4);
  ASSERT_EQ(shape.rank(), 4);
}
