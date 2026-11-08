// C++23 다차원 operator[] 예제.
// C++17까지 operator[]는 인자를 정확히 1개만 받을 수 있어서
//   - m(r, c)  : operator()로 우회하거나
//   - m[r][c]  : 행 proxy를 반환하는 식으로 우회해야 했다.
// C++23부터는 operator[]가 0개 이상의 인자를 받을 수 있다.

#include <array>
#include <cassert>
#include <concepts>
#include <cstddef>
#include <functional>
#include <iostream>
#include <numeric>
#include <vector>

// 1) 2차원: m[r, c] ----------------------------------------------------------

template <typename T>
class Matrix {
 public:
  Matrix(std::size_t rows, std::size_t cols, T init = T{})
      : rows_(rows), cols_(cols), data_(rows * cols, init) {}

  T& operator[](std::size_t r, std::size_t c) {
    assert(r < rows_ && c < cols_);
    return data_[r * cols_ + c];
  }
  const T& operator[](std::size_t r, std::size_t c) const {
    assert(r < rows_ && c < cols_);
    return data_[r * cols_ + c];
  }

  std::size_t rows() const { return rows_; }
  std::size_t cols() const { return cols_; }

 private:
  std::size_t rows_, cols_;
  std::vector<T> data_;
};

// 2) N차원: 인자 개수를 Rank와 같도록 컴파일 타임에 강제 ---------------------

template <typename T, std::size_t Rank>
class NdArray {
 public:
  explicit NdArray(std::array<std::size_t, Rank> extents)
      : extents_(extents),
        data_(std::reduce(extents.begin(), extents.end(), std::size_t{1},
                          std::multiplies<>{})) {}

  template <std::convertible_to<std::size_t>... Is>
    requires(sizeof...(Is) == Rank)
  T& operator[](Is... is) {
    return data_[offset({static_cast<std::size_t>(is)...})];
  }

  template <std::convertible_to<std::size_t>... Is>
    requires(sizeof...(Is) == Rank)
  const T& operator[](Is... is) const {
    return data_[offset({static_cast<std::size_t>(is)...})];
  }

 private:
  // row-major 오프셋
  std::size_t offset(const std::array<std::size_t, Rank>& idx) const {
    std::size_t off = 0;
    for (std::size_t i = 0; i < Rank; ++i) {
      assert(idx[i] < extents_[i]);
      off = off * extents_[i] + idx[i];
    }
    return off;
  }

  std::array<std::size_t, Rank> extents_;
  std::vector<T> data_;
};

int main() {
  Matrix<int> m(2, 3);
  for (std::size_t r = 0; r < m.rows(); ++r) {
    for (std::size_t c = 0; c < m.cols(); ++c) {
      m[r, c] = static_cast<int>(r * 10 + c);  // C++23: m[r, c]
    }
  }
  for (std::size_t r = 0; r < m.rows(); ++r) {
    for (std::size_t c = 0; c < m.cols(); ++c) std::cout << m[r, c] << ' ';
    std::cout << '\n';
  }

  NdArray<int, 3> a(std::array<std::size_t, 3>{2, 3, 4});
  a[1, 2, 3] = 42;
  a[0, 0, 0] = 7;
  std::cout << a[1, 2, 3] << ' ' << a[0, 0, 0] << '\n';
  // a[1, 2] = 0;  // 에러: 인자 개수가 Rank(3)와 다름
}
