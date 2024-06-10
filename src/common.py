# Simple implementation of a binary tree
class TreeNode:
    left = None
    right = None
    value = 0

    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value

    def as_child(self):
        return self

    def has_children(self):
        return self.left != None and self.right != None


# Return the number of items common between two lists as a percentage, rounded down
def compare_items(items_a, items_b):
    v = 0

    for a, b in zip(items_a, items_b):
        if a == b:
            v += 1

    return int(v / len(items_a) * 100)


# Print with no newline
def printf(*args):
    print(*args, end="")


# Erase the current line
def erase_line():
    printf("\r\x1B[0K\r")


# Pretty-print the compression progress
def print_progress(bytes_processed, uncomp_size, comp_size=None):
    # Prevents writing to the buffer too often
    if bytes_processed % 100 == 0:
        # Move cursor to the start of the line
        printf("\r")

        printf(f"{bytes_processed}/{uncomp_size} bytes processed")

        if comp_size:
            printf(
                f", {comp_size} bytes compressed, {100 - comp_size / bytes_processed * 100:.2f}% space saving"
            )

        # Erase the rest of the line (the previous output)
        printf("\x1B[0K")
