# Implementation of Fano coding https://en.wikipedia.org/wiki/Shannon%E2%80%93Fano_coding
import sys
import math
import random
from helpers import FormatConverter, rand_input, compute_entropy
from dataclasses import dataclass

@dataclass
class Symbol:
    byte: int
    p: float
    codeword: str = ''

class FanoCoding:
    def _partition(self, symbols: list[Symbol], lo: int, hi: int) -> None:
        if hi - lo <= 1: return
        if hi - lo == 2:
            symbols[lo].codeword += '0'
            symbols[lo+1].codeword += '1'
            return
        total = sum([s.p for i,s in enumerate(symbols) if i >= lo and i < hi])
        left_sum, minval, minidx = 0, float('inf'), lo
        # find index that partitions list
        for i in range(lo, hi):
            left_sum += symbols[i].p
            if abs(2 * left_sum - total) < minval:
                minval = abs(2 * left_sum - total) # equals difference of left and right side
                minidx = i+1
        for i in range(lo,minidx): symbols[i].codeword += '0'
        for i in range(minidx,hi): symbols[i].codeword += '1'
        self._partition(symbols, lo, minidx)
        self._partition(symbols, minidx, hi)
    def _encode(self, src: bytes, symbols: list[Symbol]) -> tuple[bytes, int]:
        encodings = { s.byte: s.codeword for s in symbols }
        return FormatConverter.bits_to_bytes("".join([encodings[b] for b in src]))
    def _decode(self, bitstr: str, decodings: dict[str,int]) -> bytes:
        decoded = []
        buffer = ''
        for bit in bitstr:
            buffer += bit
            if buffer in decodings:
                decoded.append(decodings[buffer])
                buffer = ''
        return bytes(decoded)
    def encode(self, src: bytes) -> tuple[bytes, int, dict[str,int]]:
        symbols = sorted([Symbol(b, src.count(b) / len(src)) for b in set(src)], key=lambda s: s.p, reverse=True)
        self._partition(symbols, 0, len(symbols))
        (encoded, padding) = self._encode(src, symbols)
        decodings = { s.codeword: s.byte for s in symbols }
        return (encoded, padding, decodings)
    def decode(self, b: bytes, padding: int, decodings: dict[str,int]) -> bytes:
        bitstr = FormatConverter.bytes_to_bits(b, padding)
        return self._decode(bitstr, decodings)

if __name__ == "__main__":
    input_bytes = sys.argv[1].encode('utf-8') if len(sys.argv) > 1 else rand_input()
    encoder = FanoCoding()
    (encoded, padding, decodings) = encoder.encode(input_bytes)
    decoded = encoder.decode(encoded, padding, decodings)
    print(f"Input length={len(input_bytes)} entropy={compute_entropy(input_bytes)}")
    print(f"Encoded length={len(encoded)} entropy={compute_entropy(encoded)}")
    print(f"Decoded length={len(decoded)} entropy={compute_entropy(decoded)}")
    print(f"input_bytes == decoded: {input_bytes == decoded}")
