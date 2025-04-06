# Implementation of Shannon Coding https://en.wikipedia.org/wiki/Shannon_coding
import math
import sys

class ShannonCoding:
    def _compute_probs(self, src: str) -> list[tuple[str, int]]:
        return [(c, src.count(c) / len(src)) for c in set(src)]
    def _codeword_length(self, p: float) -> int: return math.ceil(-1 * math.log2(p))
    def _increment_bin_str(self, s: str) -> str: return "{0:b}".format(int(s, 2) + 1)
    def _encode_symbols(self, lengths: list[tuple[str,int]]) -> list[tuple[str, str]]:
        prev = "-1"
        return [(c, prev := self._increment_bin_str(prev).ljust(l,'0')) for i, (c,l) in enumerate(lengths)]
    def encode(self, src: str) -> str:
        probs = sorted(self._compute_probs(src), key=lambda x: x[1], reverse=True)
        lengths = [(c, self._codeword_length(p)) for c,p in probs]
        print(lengths)
        print(self._encode_symbols(lengths))
        return src


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 shannon.py <str_to_encode>")
        sys.exit(1)

    wiki_str = "aaaaaaaaaaaaaaabbbbbbbccccccddddddeeeeee"

    input_str = sys.argv[1]
    encoder = ShannonCoding()
    encoded = encoder.encode(wiki_str)
    print(f"Input str: {input_str}")
    print(f"Encoded str: {encoded}")

