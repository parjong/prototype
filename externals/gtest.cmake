if(NOT DEFINED GTEST_URL)
  set(GTEST_URL https://github.com/google/googletest/archive/release-1.8.0.tar.gz)
endif()

ExternalSource_Download(GTEST ${GTEST_URL})

add_subdirectory(${GTEST_SOURCE_DIR} gtest)
