# Lossless Compression Techniques for Grayscale Images

This project was created as part of Memorial University's course COMP 3301: Visual Computing and Applications.

The paper and associated data can be found in the `results` directory.

## Group Members

- Amélie Butler
- Anders Cornect
- Ethan Denny
- Emily Dormody

## Purpose Of The Code

The purpose of our code is to generate data for comparisons of different lossless compression algorithms in terms of space savings and run time. The algorithms are:

- Run Length Encoding
- LZ77
- Huffman Coding
- Arithmetic Coding

## Test Images

We pulled our test images from the [UCS-SIPI database](https://sipi.usc.edu/database/database.php?volume=misc). One image (gray21.512.tiff), was excluded, as it always led to extreme outliers with LZ77 and greatly distorted our data. We will look into this in future if possible.

## A Note On C Code

We have written some of our code in C (`src/speedlib.c`) to improve performance. To run, you will need to have Linux, Python 3.10+, GCC, and Make. To compile run:.

```bash
make
```

## A Note On Dependencies

Dependency requirements are in `requirements.txt`. To install, run:

```bash
pip install -r requirements.txt
```

## How To Use

- Each algorithm compresses the image, verifies that it can return the image to the original, and then saves its run time and space savings to a CSV file.
- All inputs/input changes should be made in the config.json file. Below is a sample of a configuration. The structure is as follows:

```jsonc
    "lz77": {
        "name": "LZ77",
        "run": true,
        "args": {
            "buffer_length": 258,
            "dictionary_length": 32768
        }
    }
```

- Each JSON object is recorded in this format and order.
- The **name** value determines which compression algorithm to run as well as the output display name.
- The **args** array gives the input values to the compress functions along with the image to be compressed. This can also be blank.
- **"run"** should be a boolean value true or false to indicate whether or not the given compression algorithm will be applied to the image set. This allows the flexibility of which algorithms are running without drastically changing the configurations.
- The only values that can be edited are the boolean value "run", and in some cases, the values of the args. Both of these should maintain the same data type.
- Execute the following command: `python src/init.py`
- The selected algorithms will be used to compress each of the images, with results including trimmed and untrimmed graphs being written to the `data` folder.

## The Code Base

All code is contained in the `src` directory.

### config.json

Config settings for a given "run" of testing.

#### Example

```jsonc
{
  "rle": {
    // Name of the module this config is describing
    "name": "Run-length encoding", // Display name
    "run": true,
    "args": {} // Passed to the compress() function as **kwargs
  },
  "huffman": {
    "name": "Huffman coding",
    "run": true,
    "args": {
      "L": 256
    }
  },
  "lz77": {
    "name": "LZ77",
    "run": true,
    "args": {
      "buffer_length": 258,
      "dictionary_length": 32768
    }
  }
}
```

### init.py

`init.py` contains code that runs the algorithms, as specified in `config.json`, and then outputs their results. It dynamically imports modules, and does not need to be tinkered with, unless adjusting I/O is desired.

### [algorithm name].py

Implementation of a given algorithm. Each contains two core functions (plus worker functions):

- `compress(image: MatLike, level: int=0, **kwargs) -> int, int, int`

  This does the heavy lifting, and is the only public functions of a given algorithm. It takes a grayscale image, an optimization level, and as many named arguments as it needs for the given algorithm For example, Huffman coding requires the maximum intensity, e.g. `1` or `256`. It then returns the size of the compressed image in bytes (NOT the actual compressed image - that would make algorithms like Huffman coding unbearable to write), the result of `verify()` (see below), and the time in seconds it took to compress (but not verify) the image.

- `verify(uncompressed_bytes: numpy.ndarray, compressed_bytes: numpy.ndarray) -> int`

  Decompresses `compressed_bytes` and then compares the result DIRECTLY to `uncompressed_bytes`. It returns the percentage of matching bytes between the two, rounded down. So, a result of `100` implies that the algorithm was able to compress and decompress the bytes of a given image with perfect accuracy.
