# Implementation of Huffman coding https://en.wikipedia.org/wiki/Huffman_coding#Compression
from dataclasses import dataclass
import heapq
import sys
from typing import Optional

from helpers import FormatConverter, compute_entropy, rand_input

@dataclass
class TreeNode:
    byte: int | None
    count: int
    left: Optional["TreeNode"]
    right: Optional["TreeNode"]
    def __lt__(self, other):
        return self.count < other.count

class HuffmanCoding:
    def _create_tree(self, symbols: list[TreeNode]) -> TreeNode:
        heapq.heapify(symbols)
        while len(symbols) > 1:
            first, second = heapq.heappop(symbols), heapq.heappop(symbols)
            new_node = TreeNode(None, first.count + second.count, first, second)
            heapq.heappush(symbols,new_node)
        return heapq.heappop(symbols) # root
    def _compute_encodings(self, node: TreeNode, encodings: dict[int,str], code: str, depth: int = 0):
        if node.left != None: self._compute_encodings(node.left, encodings, code + "0", depth + 1)
        if node.right != None: self._compute_encodings(node.right, encodings, code + "1", depth + 1)
        if node.left == None and node.right == None: encodings[node.byte] = code if depth > 0 else "0"
    def _encode(self, src: bytes) -> TreeNode:
        symbols = [TreeNode(b, src.count(b), None, None) for b in set(src)]
        root = self._create_tree(symbols)
        encodings = {}
        self._compute_encodings(root, encodings, "", 0)
        decodings = {v: k for k,v in encodings.items()}
        (encoded, padding) = FormatConverter.bits_to_bytes("".join([encodings[b] for b in src]))
        return (encoded, padding, decodings)
    def _decode(self, bitstr: str, decodings: dict[str,int]) -> bytes:
            decoded = []
            buffer = ''
            for bit in bitstr:
                    buffer += bit
                    if buffer in decodings:
                            decoded.append(decodings[buffer])
                            buffer = ''
            return bytes(decoded)
    def encode(self, src: bytes) -> bytes:
        return self._encode(src)
    def decode(self, b: bytes, padding: int, decodings: dict[str,int]) -> bytes:
        bitstr = FormatConverter.bytes_to_bits(b, padding)
        return self._decode(bitstr, decodings)
    
if __name__ == "__main__":
        input_bytes = sys.argv[1].encode('utf-8') if len(sys.argv) > 1 else rand_input()
        encoder = HuffmanCoding()
        (encoded, padding, decodings) = encoder.encode(input_bytes)
        decoded = encoder.decode(encoded, padding, decodings)
        print(f"Input length={len(input_bytes)} entropy={compute_entropy(input_bytes)}")
        print(f"Encoded length={len(encoded)} entropy={compute_entropy(encoded)}")
        print(f"Decoded length={len(decoded)} entropy={compute_entropy(decoded)}")
        print(f"input_bytes == decoded: {input_bytes == decoded}")
