// c++17
#pragma once
#include <iostream>
#include <vector>

template<typename... Args>
auto sum(Args... args) {
    return (... + args);
}

// right to left: a1 + (a2 + (a3 + a4))
template<typename... Args>
void print_right(Args... args) {
    (std::cout << ... << args);
}

// left to right: ((a1 + a2) + a3) + a4
template<typename... Args>
void print_left(Args... args) {
    // xx << ... << std::cout;
}

// right to left: a1 + (a2 + (a3 + a4))
template<typename... Args>
auto sum_right(Args... args) {
    return (args + ... + 100);
}

// left to right: ((a1 + a2) + a3) + a4
template<typename... Args>
auto sum_left(Args... args) {
    return (100 + ... + args);
}

// multi_print("Hello", 123, 456, "world")
template<typename... Args>
void multi_print(Args... args) {
    (std::cout << ... << args) << std::endl;
}

template<typename... Args>
bool and_all(Args... args) {
    return (... && args);
}

template<typename... Args>
bool or_all(Args... args) {
    return (... || args);
}

template<typename T, typename... Args>
void vector_push_back(std::vector<T>& v, Args&&... args) {
    static_assert((std::is_constructible_v<T, Args&&> && ...));
    (v.push_back(std::forward<Args>(args)), ...);
}
