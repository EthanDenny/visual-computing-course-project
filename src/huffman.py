from common import TreeNode, compare_items, print_progress, erase_line

import math
import time


def compress(img, max_intensity=256):
    start = time.time()

    img_size = len(img.flatten())

    hist = [0] * max_intensity

    for row in img:
        for v in row:
            hist[v] += 1

    hist_pairs = [TreeNode(v, None, n) for (v, n) in enumerate(hist) if n > 0]
    hist_pairs.sort(reverse=True, key=lambda node: node.value)

    while len(hist_pairs) > 1:
        b = hist_pairs.pop()
        a = hist_pairs.pop()

        node = TreeNode(a.as_child(), b.as_child(), a.value + b.value)

        for i, n in enumerate(hist_pairs):
            if node.value > n.value:
                hist_pairs.insert(i + 1, node)
                break
        else:  # We love unconventional Python
            hist_pairs.append(node)

    hist_dict = {}

    def descend(node, i=0):
        if node.has_children():
            descend(node.left, 2 * i)
            descend(node.right, 2 * i + 1)
        else:
            hist_dict[node.left] = i

    descend(hist_pairs[0])

    comp_bits = ""
    bytes_processed = 0

    for row in img:
        for v in row:
            bytes_processed += 1
            comp_bits += format(hist_dict[v], "b")

            print_progress(bytes_processed, img_size, math.ceil(len(comp_bits) / 8))

    erase_line()

    end = time.time()

    size = math.ceil(len(comp_bits) / 8)  # Convert from bits to bytes

    return size, verify(img, comp_bits, hist_dict), end - start


def verify(img, comp_bits, dict):
    # Invert dictionary
    dict = {format(v, "b"): k for k, v in dict.items()}

    uncomp_bytes = img.flatten()
    decomp_bytes = []

    i = 0
    while i < len(comp_bits):
        l = 0
        while comp_bits[i : i + l] not in dict:
            l += 1
        while comp_bits[i : i + l] in dict and i + l <= len(comp_bits):
            l += 1
        l -= 1
        decomp_bytes += [dict[comp_bits[i : i + l]]]
        i += l

    return compare_items(uncomp_bytes, decomp_bytes)
