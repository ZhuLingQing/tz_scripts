#include "cpp17_lambda.hpp"

int main() {
    multi_print("Hello", 123, 456, "world");
    std::vector<int> v;
    vector_push_back(v, 1, 3, 5, 7, 9);
    for (auto &x:v)
        std::cout << x << ", ";
    std::cout << std::endl;
    return 0;
}