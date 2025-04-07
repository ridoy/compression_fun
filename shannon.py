# Implementation of Shannon Coding https://en.wikipedia.org/wiki/Shannon_coding
import math
import sys
import random
from dataclasses import dataclass

@dataclass
class Symbol:
    byte: int
    count: int
    num_bytes: int
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
    def encode(self, src: bytes) -> tuple[bytes,int,dict[str, str]]:
        symbols = { b: Symbol(byte=b, count=src.count(b), num_bytes=len(src)) for b in set(src) }
        self._compute_probs(symbols)
        self._compute_codeword_lengths(symbols)
        self._compute_cumprob(symbols)
        self._compute_encodings(symbols)
        encoded, padding = self._encode(src, symbols)
        decodings = { symbol.codeword: symbol.byte for symbol in symbols.values()}
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
        return bytes(decoded)

def compute_entropy(data: bytes) -> float:
    probs = [data.count(b) / len(data) for b in set(data)]
    entropy = 0.0
    for p in probs:
        entropy -= p * math.log2(p)
    return entropy

def rand_input(input_size: int = 1000) -> bytes:
    allowed = [ord('a'), ord('b'), ord('c')]
    return bytes(random.choice(allowed) for _ in range(input_size)) 

if __name__ == "__main__":
    input_bytes = sys.argv[1].encode('utf-8') if len(sys.argv) > 1 else rand_input()
    encoder = ShannonCoding()
    (encoded, padding, decodings) = encoder.encode(input_bytes)
    decoded = encoder.decode(encoded, padding, decodings)
    print(f"Input length={len(input_bytes)} entropy={compute_entropy(input_bytes)}")
    print(f"Encoded length={len(encoded)} entropy={compute_entropy(encoded)}")
    print(f"Decoded length={len(decoded)} entropy={compute_entropy(decoded)}")
    print(f"input_bytes == decoded: {input_bytes == decoded}")

