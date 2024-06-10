from common import compare_items, print_progress, erase_line
from fractions import Fraction

import math
import time


def compress(img):
    start = time.time()

    flat_img = img.flatten()

    unique_intensities = set(flat_img)
    freq = get_frequencies(flat_img, unique_intensities)
    intervals = create_intervals(freq)

    range_lower = Fraction(0)
    range_upper = Fraction(1)

    byte_count = 0

    for v in flat_img:
        dist = range_upper - range_lower
        this_lower, this_upper = intervals[v]
        range_upper = range_lower + this_upper * dist
        range_lower += this_lower * dist

        byte_count += 1

        print_progress(byte_count, len(flat_img))

    erase_line()

    end = time.time()

    avg = (range_upper + range_lower) / 2
    n, d = avg.as_integer_ratio()
    size = (binary_digits(n) + binary_digits(d)) / 8

    return size, verify(flat_img, avg, intervals), end - start


def binary_digits(n):
    return math.ceil(math.log(n, 10) * math.log(10, 2))


def create_intervals(freq):
    intervals = {}
    lower_bound = Fraction(0)
    upper_bound = None

    for intensity, prob in freq.items():
        upper_bound = lower_bound + prob
        intervals[intensity] = (lower_bound, upper_bound)
        lower_bound = upper_bound

    return intervals


def get_frequencies(img, unique):
    frequencies = dict.fromkeys(unique, 0)

    for value in img:
        frequencies[value] += 1

    for k, v in frequencies.items():
        frequencies[k] = Fraction(v, len(img))

    return frequencies


def verify(uncomp_bytes, comp_val, intervals):
    decomp_bytes = []

    # Invert dictionary
    intervals = {v: k for k, v in intervals.items()}

    for _ in range(len(uncomp_bytes)):
        for val_range in intervals.keys():
            lower, upper = val_range
            if lower < comp_val < upper:
                decomp_bytes.append(intervals[val_range])
                dist = upper - lower
                comp_val = (comp_val - lower) / dist
                break

    return compare_items(uncomp_bytes, decomp_bytes)
