cmake_minimum_required(VERSION 3.18)

project(Algorithms)

# Download automatically, you can also just copy the conan.cmake file
if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
   message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
   file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/master/conan.cmake"
                  "${CMAKE_BINARY_DIR}/conan.cmake")
endif()

include(${CMAKE_BINARY_DIR}/conan.cmake)
conan_cmake_run(CONANFILE conanfile.py
                BASIC_SETUP CMAKE_TARGETS
                BUILD missing)

option(BUILD_BENCHMARK "This will enable the performance tests using google benchmark" ON)
option(BUILD_TESTS "Enables Tests, required GTest" ON)

add_library(${PROJECT_NAME} INTERFACE)
add_library(Algorithms::${PROJECT_NAME} ALIAS ${PROJECT_NAME})

target_include_directories(${PROJECT_NAME} INTERFACE src/)

target_sources(${PROJECT_NAME} INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/src/sorting/bubble_sort.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/sorting/insertion_sort.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/sorting/quick_sort.hpp)

target_compile_features(${PROJECT_NAME} INTERFACE cxx_std_20)

target_compile_options(${PROJECT_NAME} INTERFACE
    $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:
        -Wall -Werror -pedantic-errors -Wextra -Wconversion -Wsign-conversion -Wno-gnu-zero-variadic-macro-arguments>
    $<$<CXX_COMPILER_ID:MSVC>:
        /WX /W4>
)

######################################################################
if(BUILD_TESTS)
    add_executable(${PROJECT_NAME}_Tests)
    
    target_sources(${PROJECT_NAME}_Tests PRIVATE 
        src/sorting/tests.cpp)

    target_link_libraries(${PROJECT_NAME}_Tests PRIVATE
        Algorithms::${PROJECT_NAME}
        CONAN_PKG::gtest
    )

    target_compile_options(${PROJECT_NAME}_Tests PRIVATE
        $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>>:
            -Wno-gnu-zero-variadic-macro-arguments>
    )

    include(GoogleTest)
    enable_testing()
    gtest_discover_tests(${PROJECT_NAME}_Tests)
endif()

######################################################################
if( BUILD_BENCHMARK)
    # Requires PThreads on Linux
    set(THREADS_PREFER_PTHREAD_FLAG ON)
    find_package(Threads REQUIRED)

    add_executable(${PROJECT_NAME}_Benchmark)

    target_sources(${PROJECT_NAME}_Benchmark PRIVATE 
        src/benchmark.cpp)

    target_include_directories(${PROJECT_NAME}_Benchmark PRIVATE
        src/benchmark)

    target_link_libraries(${PROJECT_NAME}_Benchmark PRIVATE
        Algorithms::${PROJECT_NAME}
        CONAN_PKG::benchmark
        Threads::Threads
        $<$<TARGET_EXISTS:Algorithms::${PROJECT_NAME}_Reference>:Algorithms::${PROJECT_NAME}_Reference>)

    add_custom_target(NAME ${PROJECT_NAME}_Benchmark
        COMMAND ${PROJECT_NAME}_Benchmark
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
endif()
