to make cmake ok will add 
SQLITE_INST_DIR=F:\vcpkg\installed\x64-windows

cmake -B build -DCMAKE_PREFIX_PATH=%SQLITE_INST_DIR%


edit LibeventConfig.cmake 
```cmake
    macro(find_event_lib _comp)
        unset(_event_lib_dbg CACHE)
        unset(_event_lib_rel CACHE)
        find_library(_event_lib_dbg
                    NAMES "event_${_comp}d"
                    PATHS "${_INSTALL_PREFIX}/lib")
        find_library(_event_lib_rel
                    NAMES "event_${_comp}"
                    PATHS "${_INSTALL_PREFIX}/lib")
        if(_event_lib_rel OR _event_lib_dbg)
            list(APPEND LIBEVENT_LIBRARIES "libevent::${_comp}")
            set_case_insensitive_found(${_comp})
            if(_event_lib_dbg)
                message_if_needed(STATUS "Found libevent component: ${_event_lib_dbg}")
            endif()
            if(_event_lib_rel)
                message_if_needed(STATUS "Found libevent component: ${_event_lib_rel}")
            endif()
        else()
            no_component_msg(${_comp})
        endif()
    endmacro()
```

=>
```cmake
    macro(find_event_lib _comp)
        unset(_event_lib_dbg CACHE)
        unset(_event_lib_rel CACHE)
        if(WIN32)
            find_library(_event_lib_dbg
                        NAMES "event_${_comp}d"
                        PATHS "${_INSTALL_PREFIX}/lib")
            find_library(_event_lib_rel
                        NAMES "event_${_comp}"
                        PATHS "${_INSTALL_PREFIX}/lib")
            find_library(_event_so_dbg
                        NAMES "event_${_comp}d"
                        PATHS "${_INSTALL_PREFIX}/bin")
            find_library(_event_so_rel
                        NAMES "event_${_comp}"
                        PATHS "${_INSTALL_PREFIX}/bin")
            if(_event_lib_rel OR _event_lib_dbg OR _event_so_dbg OR _event_so_rel)
                list(APPEND LIBEVENT_LIBRARIES "libevent::${_comp}")
                set_case_insensitive_found(${_comp})
                if(_event_lib_dbg)
                    message_if_needed(STATUS "Found libevent component: ${_event_lib_dbg}")
                endif()
                if(_event_lib_rel)
                    message_if_needed(STATUS "Found libevent component: ${_event_lib_rel}")
                endif()

                if(_event_so_dbg)
                    message_if_needed(STATUS "Found libevent component: ${_event_so_dbg}")
                endif()

                if(_event_so_rel)
                    message_if_needed(STATUS "Found libevent component: ${_event_so_rel}")
                endif()

            else()
                no_component_msg(${_comp})
            endif()
        else()
            find_library(_event_lib_dbg
                        NAMES "event_${_comp}d"
                        PATHS "${_INSTALL_PREFIX}/lib")
            find_library(_event_lib_rel
                        NAMES "event_${_comp}"
                        PATHS "${_INSTALL_PREFIX}/lib")
            if(_event_lib_rel OR _event_lib_dbg)
                list(APPEND LIBEVENT_LIBRARIES "libevent::${_comp}")
                set_case_insensitive_found(${_comp})
                if(_event_lib_dbg)
                    message_if_needed(STATUS "Found libevent component: ${_event_lib_dbg}")
                endif()
                if(_event_lib_rel)
                    message_if_needed(STATUS "Found libevent component: ${_event_lib_rel}")
                endif()

            else()
                no_component_msg(${_comp})
            endif()
        endif()
    endmacro()
```


copy F:\vcpkg\installed\x64-windows\bin\event_core.dll to .\build\Release to run ok

