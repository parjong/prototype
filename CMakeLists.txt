cmake_minimum_required(VERSION 3.16)

project(prototype)

# list(APPEND CMAKE_PREFIX_PATH)?
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

add_executable(sample sample.cpp)
target_include_directories(sample PRIVATE include)
