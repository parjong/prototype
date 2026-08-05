#include <iostream>
#include <cstdint>

int main() {
    // Pointer access to address 0x10 and 0x20
    volatile uint8_t *addr_10 = reinterpret_cast<volatile uint8_t *>(0x10);
    volatile uint8_t *addr_20 = reinterpret_cast<volatile uint8_t *>(0x20);

    // 0x10번지에 1을 write
    std::cout << "[sample.cpp] Writing 1 to address 0x10" << std::endl;
    *addr_10 = 1;

    // 0x20번지를 읽어서 출력
    uint8_t read_val = *addr_20;
    std::cout << "[sample.cpp] Read value from address 0x20: " << static_cast<int>(read_val) << std::endl;

    return 0;
}
