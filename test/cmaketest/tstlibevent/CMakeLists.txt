cmake_minimum_required(VERSION 3.10)
project(libevsample CXX)


list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules)
# Find Boost components
# REQUIRED makes the build fail if Boost is not found
# COMPONENTS lists the specific Boost libraries you need
find_package(Libevent 2.1.8 MODULE REQUIRED)

# Check if Boost was found successfully
if (Libevent_FOUND)
	message(STATUS "libevent found")
else()
    message(FATAL_ERROR "Libevent Set  CMAKE_PREFIX_PATH.")
endif()

message(STATUS "LIBEVENT_INCLUDE_DIRS ${LIBEVENT_INCLUDE_DIRS}")

# Include directories for Boost headers
include_directories(${LIBEVENT_INCLUDE_DIRS})

# Create an executable
add_executable(my_app main.cpp)

message(STATUS "LIBEVENT_LIBRARIES ${LIBEVENT_LIBRARIES}")
# Link Boost libraries to the executable
target_link_libraries(my_app PRIVATE ${LIBEVENT_LIBRARIES})