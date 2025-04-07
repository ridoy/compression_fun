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
    codeword: str | None = None


class FormatConverter:
    @staticmethod
    def bits_to_bytes(bitstr: str) -> tuple[bytes,int]:
        padding = ((8 - len(bitstr) % 8) % 8)
        padded = bitstr + '0' * padding
        return int(padded, 2).to_bytes(len(padded) // 8, byteorder='big'), padding
    @staticmethod
    def bytes_to_bits(b: bytes, padding: int) -> str:
        bitstr = ''.join(f'{byte:08b}' for byte in b)
        return bitstr[:len(bitstr) - padding] if padding else bitstr
    @staticmethod
    def dec_to_bin(x: float, bits: int) -> str:
        result = ''
        while bits > 0:
            x *= 2
            bit = int(x)
            result += str(bit)
            x -= bit
            bits -= 1
        return result
    

class ShannonCoding:
    def _compute_probs(self, symbols: dict[str,Symbol]) -> None:
        for symbol in symbols.values():
            symbol.prob = symbol.count / symbol.strlen
    def _codeword_length(self, p: float) -> int: return math.ceil(-1 * math.log2(p))
    def _compute_codeword_lengths(self, symbols: dict[str,Symbol]) -> None:
        for symbol in symbols.values():
            symbol.codeword_length = self._codeword_length(symbol.prob)
    def _compute_cumprob(self, symbols: dict[str,Symbol]) -> None:
        prev = 0
        for symbol in sorted(symbols.values(), key=lambda x: x.codeword_length):
            symbol.cumprob = prev
            prev += symbol.prob
    def _increment_bin_str(self, s: str) -> str: return "{0:b}".format(int(s, 2) + 1)
    def _compute_encodings(self, symbols: dict[str,Symbol]) -> None:
        for c, symbol in symbols.items():
            symbol.codeword = FormatConverter.dec_to_bin(symbol.cumprob, symbol.codeword_length)
    def _encode(self, src: str, symbols: dict[str,Symbol]) -> tuple[bytes,int]:
        return FormatConverter.bits_to_bytes("".join([symbols[c].codeword for c in src]))
    def encode(self, src: str) -> tuple[bytes,dict[str, str]]:
        symbols = { c: Symbol(c, src.count(c), len(src)) for c in set(src) }
        self._compute_probs(symbols)
        self._compute_codeword_lengths(symbols)
        self._compute_cumprob(symbols)
        self._compute_encodings(symbols)
        encoded, padding = self._encode(src, symbols)
        decodings = { symbol.codeword: symbol.char for symbol in symbols.values()}
        return (encoded, padding, decodings)
    def decode(self, b: bytes, padding: int, decodings: dict[str,str]) -> str:
        bitstr = FormatConverter.bytes_to_bits(b, padding)
        decoded = []
        buffer = ''
        for bit in bitstr:
            buffer += bit
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

