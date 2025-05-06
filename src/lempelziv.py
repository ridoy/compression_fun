import math

from helpers import FormatConverter, debug

class LZW:
    def _encode(self, src: bytes) -> tuple[bytes,int]:
        size = 256
        dictionary = {bytes([i]): i for i in range(256)}
        curr = b""
        codes = []
        for byte in src:
            if (next := curr + bytes([byte])) in dictionary:
                curr = next
            else:
                codes.append(dictionary[curr])
                dictionary[next] = size
                size += 1
                curr = bytes([byte])
        if curr:
            codes.append(dictionary[curr])
        debug(dictionary)
        bitwidth = max(9, math.ceil(math.log2(size + 1)))
        debug(bitwidth)
        bitstr = "".join([format(code, f'0{bitwidth}b') for code in codes])
        debug(" ".join([format(code, f'0{bitwidth}b') for code in codes]))
        return (bitstr, bitwidth)

    def encode(self, src: bytes) -> tuple[bytes,int,int]:
        (bitstr, bitwidth) = self._encode(src)
        (encoded, padding) = FormatConverter.bits_to_bytes(bitstr)
        return (encoded, padding, bitwidth)

    def decode(self, encoded: bytes, padding: int, bitwidth: int) -> bytes:
        bitstr = FormatConverter.bytes_to_bits(encoded, padding)

        size = 256
        dictionary = {bytes([i]): i for i in range(256)}
        curr = b""
        codes = []
        for byte in src:
            if (next := curr + bytes([byte])) in dictionary:
                curr = next
            else:
                codes.append(dictionary[curr])
                dictionary[next] = size
                size += 1
                curr = bytes([byte])
        if curr:
            codes.append(dictionary[curr])
        bitwidth = max(9, math.ceil(math.log2(size + 1)))
        debug(bitwidth)
        bitstr = "".join([format(code, f'0{bitwidth}b') for code in codes])
        debug(",".join([format(code, f'0{bitwidth}b') for code in codes]))

        return (bitstr, bitwidth)

class LZW2:
    def _encode(self, src: bytes, init_size: int = 256) -> tuple[bytes,int]:
        size, curr, codes = 256, b"", []
        dictionary = {bytes([i]): i for i in range(init_size)}
        for byte in src:
            if (next := curr + bytes([byte])) in dictionary:
                curr = next
            else:
                codes.append(dictionary[curr])
                dictionary[next] = size
                size += 1
                curr = bytes([byte])
        if curr:
            codes.append(dictionary[curr])
        bitwidth = max(9, math.ceil(math.log2(size + 1)))
        extended_bitwidth = math.floor(math.log2(size - init_size)) + 1
        bitstr = ""
        mask = ~(1 << bitwidth - 1)
        for code in codes:
            if code >> bitwidth - 1 == 1: # is extended, shave off some bits
                debug("1" + format(code & mask, f'0{extended_bitwidth}b'), end=" ")
                bitstr += "1" + format(code & mask, f'0{extended_bitwidth}b')
            else:
                debug(format(code, f'0{bitwidth}b'), end=" ")
                bitstr += format(code, f'0{bitwidth}b')
        return (bitstr, bitwidth, extended_bitwidth)

    def encode(self, src: bytes) -> tuple[bytes,int]:
        (bitstr, bitwidth, extended_bitwidth) = self._encode(src)
        (encoded, padding) = FormatConverter.bits_to_bytes(bitstr)
        return (encoded, padding, bitwidth, extended_bitwidth)


if __name__ == "__main__":
    encoder = LZW()
    encoder2 = LZW2()
    s = b"ABABABCABABABCABABABCABABABCABABABC"
    (encoded, padding, bitwidth) = encoder.encode(s)
    (encoded, padding, bitwidth, extended_bitwidth) = encoder2.encode(s)
