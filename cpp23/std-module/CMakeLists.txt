cmake_minimum_required(VERSION 3.30)

# `import std;`는 CMake에서 아직 실험 기능이라 project() 전에 UUID로 켜야 한다.
# 아래 UUID는 CMake 4.0.x 기준이다. (3.30/3.31은 다른 UUID, 4.3+는 변경될 수 있음)
set(CMAKE_EXPERIMENTAL_CXX_IMPORT_STD "d0edc3af-4c50-42ea-a356-e2862fe7a444")

project(std_module_example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_MODULE_STD ON)

add_executable(app main.cpp)
target_sources(app
  PRIVATE
    FILE_SET CXX_MODULES FILES geometry.cppm)
