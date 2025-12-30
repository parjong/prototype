function(ExternalSource_Download PREFIX URL)
  get_filename_component(FILENAME ${URL} NAME)

  set(WORKING_PATH "${CMAKE_CURRENT_BINARY_DIR}/${PREFIX}")
  set(FILE_PATH "${WORKING_PATH}/${FILENAME}")
  set(SRC_PATH "${WORKING_PATH}/src")
  set(TMP_PATH "${WORKING_PATH}/tmp")
  set(STAMP_PATH "${WORKING_PATH}/stamp")

  if(NOT EXISTS "${STAMP_PATH}")
    file(REMOVE_RECURSE "${WORKING_PATH}")

    file(MAKE_DIRECTORY "${WORKING_PATH}")
    file(MAKE_DIRECTORY "${TMP_PATH}")

    message("-- Download ${PREFIX} from ${URL}")
    file(DOWNLOAD ${URL} "${WORKING_PATH}/${FILENAME}")
    message("-- Download ${PREFIX} from ${URL} - done")

    message("-- Extract ${PREFIX}")
    execute_process(COMMAND ${CMAKE_COMMAND} -E tar xfz "${FILE_PATH}"
      WORKING_DIRECTORY "${TMP_PATH}")
    message("-- Extract ${PREFIX} - done")

    message("-- Analyze and prepare ${PREFIX}")
    file(GLOB contents "${TMP_PATH}/*")
    list(LENGTH contents n)
    if(NOT n EQUAL 1 OR NOT IS_DIRECTORY "${contents}")
      set(contents "${TMP_PATH}")
    endif()

    get_filename_component(contents ${contents} ABSOLUTE)

    file(RENAME ${contents} "${SRC_PATH}")
    message("-- Analyze and prepare ${PREFIX} - done")

    file(WRITE "${STAMP_PATH}")
  endif()

  set(${PREFIX}_SOURCE_DIR "${SRC_PATH}" PARENT_SCOPE)
endfunction()

set(ExternalSource_FOUND TRUE)
