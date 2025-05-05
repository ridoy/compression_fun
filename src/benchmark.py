import os
from fano import FanoCoding
from huffman import HuffmanCoding

# recursive list dir
def listdir(path, level=1) -> list[str]:
  files = os.listdir(path)
  paths = []
  for filename in files:
    if filename == "SHA1SUM": continue
    fullpath = f"{path}/{filename}"
    if os.path.isdir(fullpath):
      paths = paths + listdir(fullpath)
    elif level != 0:
      paths.append(fullpath)
  return paths

files = listdir('canterbury-corpus', level=0)

encoder = HuffmanCoding()

for file in files:
  print(f"Evaluating on {file}...")
  with open(file, 'rb') as f:
    data = f.read()
    (encoded, padding, decodings) = encoder.encode(data)
    decoded = encoder.decode(encoded, padding, decodings)
    msg = '\033[92msuccess\033[0m' if data == decoded else '\033[91mfailure\033[0m'
    print(msg, end=" ")
    print(f"with compression ratio: {len(data)/len(encoded)}")
