#include <iostream>
#include <boost/filesystem.hpp>
#include <boost/system/error_code.hpp>

int main() {
    boost::system::error_code ec;
    boost::filesystem::path p = "test_directory";

    if (boost::filesystem::create_directory(p, ec)) {
        std::cout << "Directory created successfully: " << p << std::endl;
    } else if (ec) {
        std::cerr << "Error creating directory: " << ec.message() << std::endl;
    } else {
        std::cout << "Directory already exists: " << p << std::endl;
    }

    return 0;
}