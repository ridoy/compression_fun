import os
from fano import FanoCoding

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

encoder = FanoCoding()

for file in files:
  with open(file, 'rb') as f:
    data = f.read()
    (encoded, padding, decodings) = encoder.encode(data)
    decoded = encoder.decode(encoded, padding, decodings)
    print(data == decoded)
