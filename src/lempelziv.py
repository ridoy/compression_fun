
class LZW:
  def _encode(self, src: bytes) -> tuple[bytes,int]:
    dictionary = {}
    i = 0
    output = []
    a = 256
    
    while i < len(src) - 1:
      curr = src[i]
      next = src[i+1]
      if bytes([curr,next] not in dictionary):
        dictionary[bytes([curr,next])] = a
        a += 1
      else:
        # found a repeat

      i += 1
    return output


  def encode(self, src: bytes) -> tuple[bytes,int]:
    self._encode(src)
    return (src,0)