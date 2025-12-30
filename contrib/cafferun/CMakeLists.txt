add_executable(cafferun cafferun.cpp)
target_link_libraries(cafferun caffe)
target_link_libraries(cafferun nnkit_nn)
