option(BUILD_PROTOBUF "Build protobuf" ON)

if(BUILD_PROTOBUF)
  find_package(Threads REQUIRED)

  ###
  ### Fetch
  ###
  if(NOT DEFINED PROTOBUF_URL)
    set(PROTOBUF_URL https://github.com/google/protobuf/archive/v3.5.1.tar.gz)
  endif()

  ExternalSource_Download(PROTOBUF ${PROTOBUF_URL})

  ###
  ### Build (copied from CMake files in protobuf/cmake)
  ###
  set(libprotobuf_lite_files
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/arena.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/arenastring.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/extension_set.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/generated_message_table_driven_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/generated_message_util.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/implicit_weak_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/coded_stream.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/zero_copy_stream.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/zero_copy_stream_impl_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/message_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/repeated_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/atomicops_internals_x86_gcc.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/atomicops_internals_x86_msvc.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/bytestream.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/common.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/int128.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/io_win32.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/once.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/status.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/statusor.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/stringpiece.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/stringprintf.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/structurally_valid.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/strutil.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/time.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/wire_format_lite.cc
    )

  set(libprotobuf_files
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/any.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/any.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/api.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/importer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/parser.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/descriptor.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/descriptor.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/descriptor_database.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/duration.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/dynamic_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/empty.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/extension_set_heavy.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/field_mask.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/generated_message_reflection.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/generated_message_table_driven.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/gzip_stream.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/printer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/strtod.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/tokenizer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/io/zero_copy_stream_impl.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/map_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/reflection_ops.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/service.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/source_context.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/struct.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/mathlimits.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/stubs/substitute.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/text_format.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/timestamp.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/type.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/unknown_field_set.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/delimited_message_util.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/field_comparator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/field_mask_util.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/datapiece.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/default_value_objectwriter.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/error_listener.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/field_mask_utility.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/json_escaping.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/json_objectwriter.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/json_stream_parser.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/object_writer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/proto_writer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/protostream_objectsource.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/protostream_objectwriter.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/type_info.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/type_info_test_helper.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/internal/utility.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/json_util.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/message_differencer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/time_util.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/util/type_resolver_util.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/wire_format.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/wrappers.pb.cc
    )

  set(libprotoc_files
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/code_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/command_line_interface.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_enum.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_enum_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_extension.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_file.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_helpers.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_map_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_padding_optimizer.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_primitive_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_service.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/cpp/cpp_string_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_doc_comment.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_enum.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_enum_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_field_base.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_helpers.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_map_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_primitive_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_reflection_class.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_repeated_enum_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_repeated_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_repeated_primitive_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_source_generator_base.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/csharp/csharp_wrapper_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_context.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_doc_comment.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_enum.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_enum_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_enum_field_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_enum_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_extension.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_extension_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_file.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_generator_factory.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_helpers.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_lazy_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_lazy_message_field_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_map_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_map_field_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_message_builder.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_message_builder_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_message_field_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_message_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_name_resolver.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_primitive_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_primitive_field_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_service.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_shared_code_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_string_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/java/java_string_field_lite.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_enum.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_enum_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_extension.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_file.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_helpers.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_map_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/javanano/javanano_primitive_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/js_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/well_known_types_embed.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_enum.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_enum_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_extension.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_file.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_helpers.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_map_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_message.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_message_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_oneof.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/objectivec/objectivec_primitive_field.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/php/php_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/plugin.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/plugin.pb.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/python/python_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/ruby/ruby_generator.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/subprocess.cc
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/zip_writer.cc
    )
 
  set(protoc_files ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/main.cc)
 
  set(js_well_known_types_sources
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/well_known_types/any.js
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/well_known_types/struct.js
    ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/well_known_types/timestamp.js)
  
  add_executable(js_embed ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/embed.cc)
  add_custom_command(
    OUTPUT ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/well_known_types_embed.cc
    DEPENDS js_embed ${js_well_known_types_sources}
    COMMAND $<TARGET_FILE:js_embed> ${js_well_known_types_sources} > ${PROTOBUF_SOURCE_DIR}/src/google/protobuf/compiler/js/well_known_types_embed.cc)

  add_library(libprotobuf ${libprotobuf_lite_files} ${libprotobuf_files})
  set_target_properties(libprotobuf PROPERTIES POSITION_INDEPENDENT_CODE True)
  target_include_directories(libprotobuf PUBLIC "${PROTOBUF_SOURCE_DIR}/src")
  target_compile_definitions(libprotobuf PRIVATE HAVE_PTHREAD)
  target_link_libraries(libprotobuf pthread)

  add_library(libprotoc ${libprotoc_files})
  target_link_libraries(libprotoc libprotobuf)
 
  add_executable(protoc ${protoc_files})
  target_link_libraries(protoc libprotobuf libprotoc)
else()
  find_package(Protobuf REQUIRED)
  
  # TODO Use IMPORTED instead of INTERFACE
  #add_library(libprotobuf SHARED IMPORTED)
  #set_property(TARGET libprotobuf PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${PROTOBUF_INCLUDE_DIRS})
  #set_property(TARGET libprotobuf PROPERTY INTERFACE_LINK_LIBRARIES ${PROTOBUF_LIBRARIES})
  add_library(libprotobuf INTERFACE)
  target_include_directories(libprotobuf INTERFACE ${PROTOBUF_INCLUDE_DIRS})
  target_link_libraries(libprotobuf INTERFACE ${PROTOBUF_LIBRARIES})

  add_executable(protoc IMPORTED GLOBAL)
  set_target_properties(protoc PROPERTIES IMPORTED_LOCATION ${PROTOBUF_PROTOC_EXECUTABLE})
endif()

### Functions
function(ProtobufProject_Generate PREFIX OUTPUT_DIR PROTO_DIR)
  get_filename_component(abs_output_dir ${OUTPUT_DIR} ABSOLUTE)
  get_filename_component(abs_proto_dir ${PROTO_DIR} ABSOLUTE)

  foreach(proto ${ARGN})
    get_filename_component(fil "${proto}" NAME)
    get_filename_component(dir "${proto}" DIRECTORY)

    get_filename_component(fil_we "${fil}" NAME_WE)

    get_filename_component(abs_fil "${abs_proto_base}/${proto}" ABSOLUTE)
    get_filename_component(abs_dir "${abs_fil}" DIRECTORY)

    list(APPEND PROTO_FILES "${abs_proto_dir}/${proto}")
    list(APPEND OUTPUT_FILES "${abs_output_dir}/${dir}/${fil_we}.pb.h")
    list(APPEND OUTPUT_FILES "${abs_output_dir}/${dir}/${fil_we}.pb.cc")
  endforeach()

  add_custom_command(OUTPUT ${OUTPUT_FILES}
                     COMMAND ${CMAKE_COMMAND} -E make_directory "${abs_output_dir}"
                     COMMAND "$<TARGET_FILE:protoc>" --cpp_out "${abs_output_dir}" -I "${abs_proto_dir}" ${PROTO_FILES})

  set(${PREFIX}_SOURCES ${OUTPUT_FILES} PARENT_SCOPE)
  set(${PREFIX}_INCLUDE_DIRS ${abs_output_dir} PARENT_SCOPE)
endfunction()
