#include <caffe/caffe.hpp>

#include <nnkit/nn/tensor/Reader.h>
#include <nnkit/nn/tensor/IndexIterator.h>

#include <iostream>

using namespace nnkit::nn;

template<typename T> class TextFormatted;

template<> class TextFormatted<tensor::Index>
{
public:
  explicit TextFormatted(const tensor::Index &index) : _index(index)
  {
    // DO NOTHING
  }

public:
  const tensor::Index &index(void) const { return _index; }

private:
  const tensor::Index &_index;
};

TextFormatted<tensor::Index> txtfmt(const tensor::Index &index)
{
  return TextFormatted<tensor::Index>{index};
}

std::ostream &operator<<(std::ostream &os, const TextFormatted<tensor::Index> &fmt)
{
  os << "(";

  if (fmt.index().rank() > 0)
  {
    os << fmt.index().at(0);

    for (uint32_t axis = 1; axis < fmt.index().rank(); ++axis)
    {
      os << ", " << fmt.index().at(axis);
    }
  }

  os << ")";

  return os;
}

class CaffeBlobReader final : public tensor::Reader<float>
{
public:
  CaffeBlobReader(const ::caffe::Blob<float> *blob) : _blob{blob}
  {
    // DO NOTHING
  }

public:
  float at(const tensor::Index &i) const override;

private:
  const ::caffe::Blob<float> * const _blob;
};

float CaffeBlobReader::at(const tensor::Index &i) const
{
  std::vector<int> indices;

  indices.resize(i.rank());
  for (uint32_t axis = 0; axis < i.rank(); ++axis)
  {
    indices.at(axis) = static_cast<int>(i.at(axis));
  }

  return *(_blob->cpu_data() + _blob->offset(indices));
}

int main(int argc, char **argv)
{
  // USAGE: cafferun [.prototxt] [.caffemodel]
  caffe::Net<float> net(argv[1], caffe::TEST);

  net.CopyTrainedLayersFrom(argv[2]);

  net.Forward();

  std::cout << "# of outputs: " << net.num_outputs() << std::endl;

  for (int n = 0; n < net.num_outputs(); ++n)
  {
    auto blob = net.output_blobs().at(n);

    std::cout << "Output #" << n << " [" << blob->shape_string() << "]" << std::endl;

    tensor::Shape shape;
    {
      const uint32_t rank = blob->shape().size();

      shape.resize(rank);
      for (uint32_t axis = 0; axis < rank; ++axis)
      {
        shape.dim(axis) = blob->shape().at(axis);
      }
    }

    CaffeBlobReader reader{blob};

    tensor::iterate(shape) << [&reader] (const tensor::Index &i)
    {
      std::cout << std::fixed << reader.at(i) << " at " << txtfmt(i) << std::endl;
    };
  }

  return 0;
}
