# Implementation of Shannon Coding https://en.wikipedia.org/wiki/Shannon_coding
import math
import sys
import random
from dataclasses import dataclass
from helpers import rand_input, compute_entropy, FormatConverter

@dataclass
class Symbol:
    byte: int
    count: int
    num_bytes: int
    prob: float | None = None
    codeword_length: int | None = None
    cumprob: float | None = None
    codeword: str | None = None


class ShannonCoding:
    def _compute_probs(self, symbols: dict[int,Symbol]) -> None:
        for symbol in symbols.values():
            symbol.prob = symbol.count / symbol.num_bytes
    def _codeword_length(self, p: float) -> int: return math.ceil(-1 * math.log2(p))
    def _compute_codeword_lengths(self, symbols: dict[int,Symbol]) -> None:
        for symbol in symbols.values():
            symbol.codeword_length = self._codeword_length(symbol.prob)
    def _compute_cumprob(self, symbols: dict[int,Symbol]) -> None:
        prev = 0
        for symbol in sorted(symbols.values(), key=lambda x: x.codeword_length):
            symbol.cumprob = prev
            prev += symbol.prob
    def _compute_encodings(self, symbols: dict[int,Symbol]) -> None:
        for c, symbol in symbols.items():
            symbol.codeword = FormatConverter.dec_to_bin(symbol.cumprob, symbol.codeword_length)
    def _encode(self, src: bytes, symbols: dict[str,Symbol]) -> tuple[bytes,int]:
        return FormatConverter.bits_to_bytes("".join([symbols[b].codeword for b in src]))
    def _decode(self, bitstr: str, decodings: dict[str,int]) -> bytes:
        decoded = []
        buffer = ''
        for bit in bitstr:
            buffer += bit
            if buffer in decodings:
                decoded.append(decodings[buffer])
                buffer = ''
        return bytes(decoded)
    def encode(self, src: bytes) -> tuple[bytes,int,dict[str,int]]:
        symbols = { b: Symbol(byte=b, count=src.count(b), num_bytes=len(src)) for b in set(src) }
        self._compute_probs(symbols)
        self._compute_codeword_lengths(symbols)
        self._compute_cumprob(symbols)
        self._compute_encodings(symbols)
        encoded, padding = self._encode(src, symbols)
        decodings = { symbol.codeword: symbol.byte for symbol in symbols.values()}
        return (encoded, padding, decodings)
    def decode(self, b: bytes, padding: int, decodings: dict[str,int]) -> bytes:
        bitstr = FormatConverter.bytes_to_bits(b, padding)
        return self._decode(bitstr, decodings)

if __name__ == "__main__":
    input_bytes = sys.argv[1].encode('utf-8') if len(sys.argv) > 1 else rand_input()
    encoder = ShannonCoding()
    (encoded, padding, decodings) = encoder.encode(input_bytes)
    decoded = encoder.decode(encoded, padding, decodings)
    print(f"Input length={len(input_bytes)} entropy={compute_entropy(input_bytes)}")
    print(f"Encoded length={len(encoded)} entropy={compute_entropy(encoded)}")
    print(f"Decoded length={len(decoded)} entropy={compute_entropy(decoded)}")
    print(f"input_bytes == decoded: {input_bytes == decoded}")

