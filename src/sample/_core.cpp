#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/iostream.h>

#include <iostream>

namespace py = pybind11;

std::string hello_from_bin() { return "Hello, world from parjong-prototype!"; }

void get_array(py::array arr)
{
  py::scoped_ostream_redirect stream(
  	std::cout,                                // std::ostream&
    py::module_::import("sys").attr("stdout") // Python output
  );

  py::buffer_info buf = arr.request();

  // Example: print shape
  std::cout << "Array shape: ";
  for (auto s : buf.shape) {
    std::cout << s << " ";
  }
  std::cout << std::endl;

  std::cout << "number of elements in arr: " << arr.size() << std::endl;

  std::cout << "format: " << buf.format << std::endl;

  if (not buf.item_type_is_equivalent_to<float>())
  {
    return;
  }
  std::cout << "float array" << std::endl;
  auto float_arr = arr.cast<py::array_t<float>>();

  // Q. How to handle N-dimensional?
  //
  // 1. Iterate over '[0, arr.size)'
  // 2. Re-constructr N-dimensional index
  if (arr.ndim() != 2) 
  {
    return;
  }

  for (ssize_t d0 = 0; d0 < arr.shape(0); ++d0)
  {
    for (ssize_t d1 = 0; d1 < arr.shape(1); ++d1)
    {
      std::cout << "arr[" << d0 << "," << d1 << "] = " << float_arr.at(d0, d1) << std::endl;
    }
  }
}

PYBIND11_MODULE(_core, m) {
  m.doc() = "pybind11 hello module";

  m.def("hello_from_bin", &hello_from_bin, R"pbdoc(
      A function that returns a Hello string.
  )pbdoc");

  m.def("get_array", &get_array);
}
