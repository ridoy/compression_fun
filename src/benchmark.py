import os
import sys
import time

from fano import FanoCoding
from huffman import HuffmanCoding
from shannon import ShannonCoding

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


def evaluate(encoder, filepath: str):
    encoder = ShannonCoding()
    with open(filepath, 'rb') as f:
        data = f.read()

        start = time.time()
        (encoded, padding, decodings) = encoder.encode(data)
        encoding_time = "{:.5f}".format(time.time() - start)
        print(f"Encoding time = {encoding_time}s | ", end="")

        start = time.time()
        decoded = encoder.decode(encoded, padding, decodings)
        decoding_time = "{:.5f}".format(time.time() - start)
        print(f"Decoding time = {decoding_time}s | ", end="")

        compression_ratio = "{:.5f}".format(len(data)/len(encoded))
        print(f"Compression ratio: {compression_ratio} | ", end="")

        print('\033[92msuccess\033[0m' if data == decoded else '\033[91mfailure\033[0m')


if __name__ == "__main__":
    shannon = ShannonCoding()
    fano = FanoCoding()
    huffman = HuffmanCoding()
    if len(sys.argv) > 1:
        evaluate(shannon, sys.argv[1])
        evaluate(fano, sys.argv[1])
        evaluate(huffman, sys.argv[1])
    else:
        filepaths = listdir('canterbury-corpus', level=0)
        for filepath in filepaths:
            print(filepath)
            print(f"Shannon: ", end="")
            evaluate(shannon, filepath)
            print(f"Fano: ", end="   ")
            evaluate(fano, filepath)
            print(f"Huffman: ", end="")
            evaluate(huffman, filepath)
            print()

