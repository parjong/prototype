cmake_minimum_required(VERSION 3.5)

project(nnkit)

enable_testing()

set(CMAKE_CXX_STANDARD 11)

function(nnkit_find_package PREFIX)
  find_package(${PREFIX} CONFIG PATHS ${CMAKE_SOURCE_DIR}/cmake ${ARGN})
endfunction(nnkit_find_package)

nnkit_find_package(ExternalSource REQUIRED)

function(envoption PREFIX DEFAULT_VALUE)
  set(VALUE ${DEFAULT_VALUE})

  if(DEFINED ENV{${PREFIX}})
    set(VALUE $ENV{${PREFIX}})
  endif()

  set(${PREFIX} ${VALUE} PARENT_SCOPE)
endfunction(envoption)

add_subdirectory(externals)
add_subdirectory(frameworks)
add_subdirectory(libs)
add_subdirectory(contrib)
