from common import compare_items, print_progress, erase_line

import speedy
import time


def compress(img, buffer_length=258, dictionary_length=32768):
    start = time.time()

    bstr = img.flatten()
    tuples = []

    buf_index = 0

    byte_count = 0

    while buf_index < len(bstr):
        dic_index = max(0, buf_index - dictionary_length)

        dic = bstr[dic_index:buf_index]
        buf = bstr[buf_index : buf_index + buffer_length]

        d, l = speedy.find_match(dic, buf)

        if l < 3:
            tuples.append((0, bstr[buf_index]))
            buf_index += 1
        else:
            tuples.append((d, l))
            buf_index += l

        byte_count += 2

        print_progress(buf_index, len(bstr), byte_count)

    erase_line()

    end = time.time()

    return byte_count, verify(bstr, tuples), end - start


def verify(img_bytes, tuples):
    final_bytes = []

    i = 0
    for a, b in tuples:
        if a > 0:
            j = i - a

            while j < i - a + b:
                final_bytes.append(final_bytes[j])
                j += 1

            i += b
        else:
            final_bytes.append(b)
            i += 1

    return compare_items(img_bytes, final_bytes)


# DEPRECATED, use speedy.find_match()
def find_match(dic, buf):
    potential_indices = [i for i in range(len(dic)) if dic[i] == buf[0]]

    if len(potential_indices) == 0:
        return (0, 0)

    next_indices = []

    for l in range(2, len(buf) + 1):
        for i in potential_indices:
            if i <= len(dic) - l:
                if dic[i + l - 1] == buf[l - 1]:
                    next_indices.append(i)
            else:
                break

        if len(next_indices) == 0:
            return len(dic) - potential_indices[0], l - 1

        potential_indices = next_indices
        next_indices = []

    return len(dic) - potential_indices[0], len(buf)
