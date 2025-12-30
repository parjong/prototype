envoption(FLATBUFFERS_URL https://github.com/google/flatbuffers/archive/v1.9.0.tar.gz)

ExternalSource_Download(FLATBUFFERS ${FLATBUFFERS_URL})

set(FlatBuffers_Library_SRCS
  ${FLATBUFFERS_SOURCE_DIR}/src/code_generators.cpp
  ${FLATBUFFERS_SOURCE_DIR}/src/idl_parser.cpp
  ${FLATBUFFERS_SOURCE_DIR}/src/idl_gen_text.cpp
  ${FLATBUFFERS_SOURCE_DIR}/src/reflection.cpp
  ${FLATBUFFERS_SOURCE_DIR}/src/util.cpp
)
add_library(flatbuffers STATIC ${FlatBuffers_Library_SRCS})
target_include_directories(flatbuffers PUBLIC ${FLATBUFFERS_SOURCE_DIR}/include)
