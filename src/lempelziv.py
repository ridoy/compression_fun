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
    return (bitstr, bitwidth)

  def encode(self, src: bytes) -> tuple[bytes,int,int]:
    (bitstr, bitwidth) = self._encode(src)
    (encoded, padding) = FormatConverter.bits_to_bytes(bitstr)
    return (encoded, padding, bitwidth)

class LZW2:
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
    for k,v in dictionary.items():
      print(int.from_bytes(k, byteorder="big"))
      print(k)
      if int.from_bytes(k, byteorder="big") >= 256:
        print(f"{k}: {v}")
    bitstr = "".join([format(code, f'0{bitwidth}b') for code in codes])
    return (bitstr, bitwidth)

  def encode(self, src: bytes) -> tuple[bytes,int]:
    (bitstr, bitwidth) = self._encode(src)
    (encoded, padding) = FormatConverter.bits_to_bytes(bitstr)
    return (encoded, padding, bitwidth)


if __name__ == "__main__":
  encoder = LZW2()
  (encoded, padding, bitwidth) = encoder.encode(b"tobeornottobe")
  print(encoded)