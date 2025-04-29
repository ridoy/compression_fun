import math

from helpers import FormatConverter

class LZW:
  def _encode(self, src: bytes) -> tuple[bytes,int]:
    size = 256
    dictionary = {bytes([i]): i for i in range(256)}
    curr = b""
    codes = []
    for byte in src:
      if (next := curr + bytes([byte])) in dictionary:
        curr = next
      else:
        codes.append(dictionary[curr])
        dictionary[next] = size
        size += 1
        curr = bytes([byte])
    if curr:
      codes.append(dictionary[curr])
    bitwidth = max(9, math.ceil(math.log2(size + 1)))
    print(bitwidth)
    bitstr = "".join([format(code, f'0{bitwidth}b') for code in codes])
    print(bitstr)
    return (bitstr, bitwidth)

  def encode(self, src: bytes) -> tuple[bytes,int,int]:
    (bitstr, bitwidth) = self._encode(src)
    (encoded, padding) = FormatConverter.bits_to_bytes(bitstr)
    return (encoded, padding, bitwidth)

class LZW2:
  def _encode(self, src: bytes, init_size: int = 256) -> tuple[bytes,int]:
    size, curr, codes = 256, b"", []
    dictionary = {bytes([i]): i for i in range(init_size)}
    for byte in src:
      if (next := curr + bytes([byte])) in dictionary:
        curr = next
      else:
        codes.append(dictionary[curr])
        dictionary[next] = size
        size += 1
        curr = bytes([byte])
    if curr:
      codes.append(dictionary[curr])
    bitwidth = max(9, math.ceil(math.log2(size + 1)))
    extended_bitwidth = math.floor(math.log2(size - init_size)) + 1
    bitstr = ""
    mask = ~(1 << bitwidth - 1)
    for code in codes:
      if code >> bitwidth - 1 == 1: # is extended, shave off some bits
        bitstr += "1" + format(code & mask, f'0{extended_bitwidth}b')
      else:
        bitstr += format(code, f'0{bitwidth}b')
    print(bitstr)
    return (bitstr, bitwidth)

  def encode(self, src: bytes) -> tuple[bytes,int]:
    (bitstr, bitwidth) = self._encode(src)
    (encoded, padding) = FormatConverter.bits_to_bytes(bitstr)
    return (encoded, padding, bitwidth)


if __name__ == "__main__":
  encoder = LZW()
  encoder2 = LZW2()
  (encoded, padding, bitwidth) = encoder.encode(b"tobeornottobe")
  print(encoded)
  (encoded, padding, bitwidth) = encoder2.encode(b"tobeornottobe")
  print(encoded)