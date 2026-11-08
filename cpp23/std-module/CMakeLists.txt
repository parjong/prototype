cmake_minimum_required(VERSION 3.30)

# `import std;`는 CMake 3.30~4.1에서는 실험 기능이라 project() 전에 UUID를 설정해야 한다.
# (4.2 이상에서는 정식 기능이므로 이 줄이 필요 없을 수 있다.)
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
