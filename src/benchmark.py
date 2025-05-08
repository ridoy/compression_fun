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

# TODO: move evaluation logic into the class it evaluates
def evaluate_shannon(filepath: str):
    encoder = ShannonCoding()
    print(f"Evaluating Shannon Coding on {filepath}...")
    with open(filepath, 'rb') as f:
        data = f.read()
        (encoded, padding, decodings) = encoder.encode(data)
        decoded = encoder.decode(encoded, padding, decodings)
        msg = '\033[92msuccess\033[0m' if data == decoded else '\033[91mfailure\033[0m'
        print(msg, end=" ")
        print(f"with compression ratio: {len(data)/len(encoded)}")


def evaluate_fano(filepath: str):
    encoder = FanoCoding()
    print(f"Evaluating Fano Coding on {filepath}...")
    with open(filepath, 'rb') as f:
        data = f.read()
        (encoded, padding, decodings) = encoder.encode(data)
        decoded = encoder.decode(encoded, padding, decodings)
        msg = '\033[92msuccess\033[0m' if data == decoded else '\033[91mfailure\033[0m'
        print(msg, end=" ")
        print(f"with compression ratio: {len(data)/len(encoded)}")


def evaluate_huffman(filepath: str):
    encoder = HuffmanCoding()
    print(f"Evaluating Huffman Coding on {filepath}...")
    with open(filepath, 'rb') as f:
        data = f.read()
        (encoded, padding, decodings) = encoder.encode(data)
        decoded = encoder.decode(encoded, padding, decodings)
        msg = '\033[92msuccess\033[0m' if data == decoded else '\033[91mfailure\033[0m'
        print(msg, end=" ")
        print(f"with compression ratio: {len(data)/len(encoded)}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start = time.time()
        evaluate_fano(sys.argv[1])
        print(f"Took {time.time() - start} seconds")
        start = time.time()
        evaluate_huffman(sys.argv[1])
        print(f"Took {time.time() - start} seconds")
    else:
        filepaths = listdir('canterbury-corpus', level=0)
        for filepath in filepaths:
            start = time.time()
            evaluate_fano(filepath)
            print(f"Took {time.time() - start} seconds")
            start = time.time()
            evaluate_huffman(filepath)
            print(f"Took {time.time() - start} seconds")
