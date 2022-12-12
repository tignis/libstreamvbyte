#include "zigzag_decode_scalar.hpp"
#include "streamvbyte.h"
#include <vector>

#if defined(_MSC_VER) && defined(_M_AMD64)
#include "zigzag_decode_ssse3.hpp"
#elif defined(__SSSE3__)
#include "zigzag_decode_ssse3.hpp"
#endif

void streamvbyte::zigzag_decode(const uint32_t* in, std::size_t count, int32_t* out) {

#if defined(_MSC_VER) && defined(_M_AMD64)
    zigzag_decode_ssse3(in, count, out); // side effect: count, out are modified
#elif defined(__SSSE3__)
    zigzag_decode_ssse3(in, count, out); // side effect: count, out are modified
#endif

    zigzag_decode_scalar(in, count, out); // side effect: count, out are modified
}

std::vector<int32_t> streamvbyte::zigzag_decode(const std::vector<uint32_t>& in) {
    std::vector<int32_t> out(in.size());
    zigzag_decode(in.data(), in.size(), out.data());
    return out;
}