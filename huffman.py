import heapq
import sys
from dataclasses import dataclass

from helpers import compute_entropy, rand_input

@dataclass
class TreeNode:
  byte: int
  left: TreeNode
  right: TreeNode

class HuffmanCoding:
  def _encode(self, src: bytes) -> bytes:
    symbols = [(src.count(b), b) for b in set(src)]
    heapq.heapify(symbols)
    while len(symbols) > 0:
      print(heapq.heappop(symbols))
  def encode(self, src: bytes) -> bytes:
    self._encode(src)
    return (src, 0, {})
  def decode(self, b: bytes, padding: int, decodings: dict[str,int]) -> bytes:
    return b
  
if __name__ == "__main__":
    input_bytes = sys.argv[1].encode('utf-8') if len(sys.argv) > 1 else rand_input()
    encoder = HuffmanCoding()
    (encoded, padding, decodings) = encoder.encode(input_bytes)
    decoded = encoder.decode(encoded, padding, decodings)
    print(f"Input length={len(input_bytes)} entropy={compute_entropy(input_bytes)}")
    print(f"Encoded length={len(encoded)} entropy={compute_entropy(encoded)}")
    print(f"Decoded length={len(decoded)} entropy={compute_entropy(decoded)}")
    print(f"input_bytes == decoded: {input_bytes == decoded}")
