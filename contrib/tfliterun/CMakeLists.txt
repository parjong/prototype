file(GLOB_RECURSE SOURCES "src/*.cpp")

add_executable(tflite "${SOURCES}")
target_link_libraries(tflite tensorflow_lite)
