#pragma once

#include <iostream>
#include <vector>

namespace streamvbyte {
/*
    Encodes a sequence of 32-bit unsigned integers to a byte array.

    @param in: a sequence of 32-bit unsigned integers
    @param count: the number of unsigned integers to encode
    @param out: a byte array

    @return the number of bytes written to out
*/
std::size_t encode(const uint32_t* in, std::size_t count, uint8_t* out);
std::vector<uint8_t> encode(const std::vector<uint32_t>& in);

/*
    Decodes a sequence of 32-bit unsigned integers from a byte array.

    @param in: a byte array
    @param out: a sequence of 32-bit unsigned integers
    @param count: the number of unsigned integers to decode

    @return the number of bytes written to in
*/
std::size_t decode(const uint8_t* in, uint32_t* out, std::size_t count);
std::vector<uint32_t> decode(const std::vector<uint8_t>& in, std::size_t size);

static inline size_t max_compressed_size(const uint32_t size) {
    return (size + 3) / 4 + size * sizeof(uint32_t);
}
}