import random
import math
import os

def debug(s: str, end: str = "\n"):
    if os.getenv("DEBUG") == "1":
        print(s, end=end)

def compute_entropy(data: bytes) -> float:
    probs = [data.count(b) / len(data) for b in set(data)]
    entropy = 0.0
    for p in probs:
        entropy -= p * math.log2(p)
    return entropy

def rand_input(input_size: int = 1000) -> bytes:
    allowed = [ord('a'), ord('b'), ord('c')]
    return bytes(random.choice(allowed) for _ in range(input_size)) 

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
