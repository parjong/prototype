find_package(ExternalSource CONFIG REQUIRED)

###
### URL for external dependencies comes from 'tensorflow/workspace.bzl'
###
set(TF_EIGEN_URL https://mirror.bazel.build/bitbucket.org/eigen/eigen/get/2355b229ea4c.tar.gz)
set(TF_GEMMLOWP_URL https://mirror.bazel.build/github.com/google/gemmlowp/archive/7c7c744640ddc3d0af18fb245b4d23228813a71b.zip)
set(TF_FARMHASH_URL https://mirror.bazel.build/github.com/google/farmhash/archive/816a4ae622e964763ca0862d9dbd19324a1eaf45.tar.gz)

# Eigen 3
ExternalSource_Download(EIGEN "${TF_EIGEN_URL}")

add_library(eigen3 INTERFACE)
target_include_directories(eigen3 INTERFACE "${EIGEN_SOURCE_DIR}")

# GEMM Low-Precision
ExternalSource_Download(GEMMLOWP "${TF_GEMMLOWP_URL}")

add_library(gemmlowp INTERFACE)
target_include_directories(gemmlowp INTERFACE "${GEMMLOWP_SOURCE_DIR}")
target_compile_definitions(gemmlowp INTERFACE GEMMLOWP_ALLOW_SLOW_SCALAR_FALLBACK)

# farmhash
ExternalSource_Download(FARMHASH "${TF_FARMHASH_URL}")

add_library(farmhash "${FARMHASH_SOURCE_DIR}/src/farmhash.cc")
target_include_directories(farmhash PUBLIC "${FARMHASH_SOURCE_DIR}/src")

###
### TensorFlow
###
set(TENSORFLOW_PATH ${CMAKE_CURRENT_SOURCE_DIR}/tensorflow)

###
### TensorFlow Lite
###
set(TENSORFLOW_LITE_PATH ${TENSORFLOW_PATH}/tensorflow/contrib/lite)

file(GLOB TFLITE_CORE_SOURCES "${TENSORFLOW_LITE_PATH}/*.c" "${TENSORFLOW_LITE_PATH}/*.cc")
file(GLOB TFLITE_CORE_TESTS "${TENSORFLOW_LITE_PATH}/*test*.cc")
list(REMOVE_ITEM TFLITE_CORE_SOURCES ${TFLITE_CORE_TESTS})

file(GLOB_RECURSE TFLITE_KERNEL_SOURCES "${TENSORFLOW_LITE_PATH}/kernels/*.cc")
# This kernel implementation uses assert without including assert.h which results in build error
list(REMOVE_ITEM TFLITE_KERNEL_SOURCES "${TENSORFLOW_LITE_PATH}/kernels/internal/spectrogram.cc")
file(GLOB_RECURSE TFLITE_KERNEL_TESTS "${TENSORFLOW_LITE_PATH}/kernels/*test*.cc")
list(REMOVE_ITEM TFLITE_KERNEL_SOURCES ${TFLITE_KERNEL_TESTS})

add_library(tensorflow_lite ${TFLITE_CORE_SOURCES} ${TFLITE_KERNEL_SOURCES})
target_include_directories(tensorflow_lite PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/tensorflow)
target_link_libraries(tensorflow_lite flatbuffers)
target_link_libraries(tensorflow_lite eigen3)
target_link_libraries(tensorflow_lite gemmlowp)
target_link_libraries(tensorflow_lite farmhash)
target_link_libraries(tensorflow_lite pthread)
target_link_libraries(tensorflow_lite dl)
