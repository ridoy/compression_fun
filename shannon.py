# Implementation of Shannon Coding https://en.wikipedia.org/wiki/Shannon_coding
import math
import sys

class ShannonCoding:
    def _compute_probs(self, src: str) -> list[tuple[str, int]]:
        return [(c, src.count(c) / len(src)) for c in set(src)]
    def _codeword_length(self, p: float) -> int: return math.ceil(-1 * math.log2(p))
    def _increment_bin_str(self, s: str) -> str: return "{0:b}".format(int(s, 2) + 1)
    def _encode_symbols(self, lengths: list[tuple[str,int]]) -> dict[str,str]:
        prev = "-1"
        result = {}
        for c,l in lengths:
            prev = self._increment_bin_str(prev).ljust(l,'0')
            result[c] = prev
        return result
    def _bits_to_bytes(self, bitstr: str) -> bytes:
        padded = bitstr + '0' * ((8 - len(bitstr) % 8) % 8)
        return int(padded, 2).to_bytes(len(padded) // 8, byteorder='big')
    def _encode(self, src: str, encodings: dict[str,str]) -> bytes:
        return self._bits_to_bytes("".join([encodings[c] for c in src]))
    def encode(self, src: str) -> tuple[bytes,dict[str, str]]:
        probs = sorted(self._compute_probs(src), key=lambda x: x[1], reverse=True)
        lengths = [(c, self._codeword_length(p)) for c,p in probs]
        encodings = self._encode_symbols(lengths)
        return (self._encode(src, encodings), encodings)

if __name__ == "__main__":
    encoder = ShannonCoding()
    (encoded, encodings) = encoder.encode(wiki_str)
    print(f"Input str: {input_str}")
    print(f"Encoded str: {encoded}")

