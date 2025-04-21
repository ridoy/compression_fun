import math

from helpers import FormatConverter

class LZW:
  def _encode(self, src: bytes) -> tuple[bytes,int]:
    size = 256
    dictionary = {bytes([i]): i for i in range(256)}
    w = b""
    codes = []
    for byte in src:
      wc = w + bytes([byte])
      if wc in dictionary:
        w = wc
      else:
        codes.append(dictionary[w])
        dictionary[wc] = size
        size += 1
        w = bytes([byte])
    if w:
      codes.append(dictionary[w])
    max_code = max(codes)
    bit_width = max(9, math.ceil(math.log2(max_code + 1)))
    bitstr = "".join([format(code, f'0{bit_width}b') for code in codes])
    return FormatConverter.bits_to_bytes(bitstr), bit_width


  def encode(self, src: bytes) -> tuple[bytes,int]:
    return self._encode(src)
