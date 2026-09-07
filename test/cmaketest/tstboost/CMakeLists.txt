cmake_minimum_required(VERSION 3.10)
project(BoostExample CXX)

# Find Boost components
# REQUIRED makes the build fail if Boost is not found
# COMPONENTS lists the specific Boost libraries you need
find_package(Boost 1.70.0 REQUIRED COMPONENTS system filesystem)

# Check if Boost was found successfully
if (Boost_FOUND)
    message(STATUS "Boost found: ${Boost_INCLUDE_DIRS}")
    message(STATUS "Boost libraries: ${Boost_LIBRARIES}")
else()
    message(FATAL_ERROR "Boost not found. Please set Boost_ROOT or CMAKE_PREFIX_PATH.")
endif()

# Include directories for Boost headers
include_directories(${Boost_INCLUDE_DIRS})

# Create an executable
add_executable(my_app main.cpp)

# Link Boost libraries to the executable
target_link_libraries(my_app PRIVATE ${Boost_LIBRARIES})