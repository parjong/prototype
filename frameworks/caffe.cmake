###
### Caffe Protocol Buffer Library
###
ProtobufProject_Generate(CAFFE_PROTO "${CMAKE_CURRENT_BINARY_DIR}/caffe" "caffe/src" "caffe/proto/caffe.proto")

add_library(caffeproto SHARED ${CAFFE_PROTO_SOURCES})
target_include_directories(caffeproto PUBLIC ${CAFFE_PROTO_INCLUDE_DIRS})
target_link_libraries(caffeproto libprotobuf)

###
### Caffe Shared Library
###
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/caffe/cmake/Modules)

find_package(Boost 1.54 REQUIRED COMPONENTS system thread filesystem)
find_package(HDF5 COMPONENTS HL REQUIRED)
find_package(Atlas REQUIRED)
find_package(Glog REQUIRED)
find_package(GFlags REQUIRED)

file(GLOB CORE_SOURCES "caffe/src/caffe/*.cpp" "caffe/src/caffe/util/*.cpp")
file(GLOB LAYER_SOURCES "caffe/src/caffe/layers/*.cpp")
file(GLOB SOLVER_SOURCES "caffe/src/caffe/solvers/*.cpp")

add_library(caffe SHARED ${CORE_SOURCES} ${LAYER_SOURCES} ${SOLVER_SOURCES})
target_compile_definitions(caffe PUBLIC CPU_ONLY)
target_include_directories(caffe PUBLIC caffe/include)
target_include_directories(caffe PRIVATE ${Boost_INCLUDE_DIRS})
target_include_directories(caffe PRIVATE ${GLOG_INCLUDE_DIRS})
target_include_directories(caffe PRIVATE ${GFLAGS_INCLUDE_DIRS})
target_include_directories(caffe PRIVATE ${HDF5_INCLUDE_DIRS})
target_include_directories(caffe PRIVATE ${Atlas_INCLUDE_DIRS})
target_link_libraries(caffe caffeproto)
target_link_libraries(caffe ${GLOG_LIBRARIES})
target_link_libraries(caffe ${GFLAGS_LIBRARIES})
target_link_libraries(caffe ${Boost_LIBRARIES})
target_link_libraries(caffe ${HDF5_LIBRARIES} ${HDF5_HL_LIBRARIES})
target_link_libraries(caffe ${Atlas_LIBRARIES})
