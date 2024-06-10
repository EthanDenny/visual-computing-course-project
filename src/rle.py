from common import compare_items, print_progress, erase_line

import time


def compress(img, max_intensity=256):
    start = time.time()

    comp_bytes = []

    img_size = len(img.flatten())

    for row in img:
        row = list(row)

        comp_v = row[0]
        index = 0
        run_length = 0

        comp_row = []

        while index + run_length < len(row):
            v = row[index + run_length]

            if v != comp_v or run_length == max_intensity - 1:
                comp_row += [comp_v, run_length]
                index += run_length
                run_length = 0
                comp_v = v
            else:
                run_length += 1

        if run_length > 0:
            comp_row += [comp_v, run_length]

        if len(comp_row) > len(row):
            comp_bytes += [0]  # Uncompressed block
            comp_bytes += row
        else:
            comp_bytes += [1]  # Compressed block
            comp_bytes += comp_row

        print_progress(len(comp_bytes), img_size)

    erase_line()

    end = time.time()

    return len(comp_bytes), verify(img, comp_bytes), end - start


def verify(img, comp_bytes):
    uncomp_bytes = img.flatten()

    row_len = len(img[0])

    decomp_bytes = []

    j = 0
    while j < len(comp_bytes):
        row = []

        j += 1

        match comp_bytes[j - 1]:
            case 0:
                row = comp_bytes[j : j + row_len]
                j += row_len
            case 1:
                while len(row) < row_len:
                    row += [comp_bytes[j]] * comp_bytes[j + 1]
                    j += 2
            case _:
                raise Exception(
                    "Something has gone catastrophically wrong with RLE. Please turn it off in config.json"
                )

        decomp_bytes += row

    return compare_items(uncomp_bytes, decomp_bytes)
