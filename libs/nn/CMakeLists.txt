file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE TESTS "src/*.test.cpp")
list(REMOVE_ITEM SOURCES ${TESTS})

add_library(nnkit_nn ${SOURCES})
target_include_directories(nnkit_nn PUBLIC include)

add_executable(nnkit_nn_test ${TESTS})
target_link_libraries(nnkit_nn_test nnkit_nn)
target_link_libraries(nnkit_nn_test gtest_main)
add_test(nnkit_nn_test nnkit_nn_test)
