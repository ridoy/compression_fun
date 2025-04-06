# Implementation of Shannon Coding https://en.wikipedia.org/wiki/Shannon_coding
import math
import sys

class ShannonCoding:
    def encode(self, src: str):
        return src

    def codeword_length(self, p: float) -> int: return math.ceil(-1 * math.log2(p))




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 shannon.py <str_to_encode>")
        sys.exit(1)

    input_str = sys.argv[1]
    encoder = ShannonCoding()
    encoded = encoder.encode(input_str)
    print(f"Input str: {input_str}")
    print(f"Encoded str: {encoded}")

