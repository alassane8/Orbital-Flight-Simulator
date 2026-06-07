cmake_minimum_required(VERSION 3.15)
project(orbital_core)

set(CMAKE_CXX_STANDARD 17)

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 REQUIRED)

pybind11_add_module(orbital_core
    orbital_core.cpp
    bindings.cpp
)

target_include_directories(orbital_core PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})