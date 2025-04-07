# Implementation of Shannon Coding https://en.wikipedia.org/wiki/Shannon_coding
import math
import sys
from dataclasses import dataclass

@dataclass
class Symbol:
    char: str
    count: int
    strlen: int
    prob: float | None = None
    codeword_length: int | None = None
    cumprob: float | None = None

class ShannonCoding:
    def _compute_probs(self, src: dict[str,Symbol]) -> None:
        for symbol in src.values():
            symbol.prob = symbol.count / symbol.strlen
    def _codeword_length(self, p: float) -> int: return math.ceil(-1 * math.log2(p))
    def _compute_codeword_lengths(self, src: dict[str,Symbol]) -> None:
        for symbol in src.values():
            symbol.codeword_length = self._codeword_length(symbol.prob)
    def _increment_bin_str(self, s: str) -> str: return "{0:b}".format(int(s, 2) + 1)
    def _encode_symbols(self, lengths: list[tuple[str,int]]) -> dict[str,str]:
        prev = "-1"
        result = {}
        for c,l in lengths:
            prev = self._increment_bin_str(prev).ljust(l,'0')
            result[c] = prev
        return result
    def _bits_to_bytes(self, bitstr: str) -> tuple[bytes,int]:
        padding = ((8 - len(bitstr) % 8) % 8)
        padded = bitstr + '0' * padding
        return int(padded, 2).to_bytes(len(padded) // 8, byteorder='big'), padding
    def _bytes_to_bits(self, b: bytes, padding: int) -> str:
        bitstr = ''.join(f'{byte:08b}' for byte in b)
        return bitstr[:len(bitstr) - padding] if padding else bitstr
    def _dec_to_bin(self, x: float, bits: int) -> str:
        result = ''
        while bits > 0:
            x *= 2
            bit = int(x)
            result += str(bit)
            x -= hit
            bits -= 1
        return result
    def _encode(self, src: str, encodings: dict[str,str]) -> bytes:
        return self._bits_to_bytes("".join([encodings[c] for c in src]))
    def encode(self, src: str) -> tuple[bytes,dict[str, str]]:
        symbols = { c: Symbol(c, src.count(c), len(src)) for c in set(src) }
        self._compute_probs(symbols)
        self._compute_codeword_lengths(symbols)
        encodings = self._encode_symbols(lengths)
        encoded, padding = self._encode(src, encodings)
        decodings = {v: k for k,v in encodings.items()}
        return (encoded, padding, decodings)
    def decode(self, b: bytes, padding: int, decodings: dict[str,str]) -> str:
        bitstr = self._bytes_to_bits(b, padding)
        decoded = []
        buffer = ''
        print(decodings)
        print(bitstr)
        for bit in bitstr:
            buffer += bit
            print(buffer)
            if buffer in decodings:
                decoded.append(decodings[buffer])
                buffer = ''
        return ''.join(decoded)

if __name__ == "__main__":
    input_str = "this is an input string"
    encoder = ShannonCoding()
    (encoded, padding, decodings) = encoder.encode(input_str)
    print(f"Input str: {input_str}")
    print(f"Encoded str: {encoded}")
    print(f"Decoded str: {encoder.decode(encoded, padding, decodings)}")

