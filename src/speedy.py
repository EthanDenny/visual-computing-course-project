import ctypes
import numpy as np

LIB_LOCALE = "./bin/speedylib.so"

try:
    lib = ctypes.CDLL(LIB_LOCALE)
except OSError:
    raise Exception(f'Could not load {LIB_LOCALE}, please run "make"')

lib.find_match.argtypes = [
    np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags="C_CONTIGUOUS"),
    ctypes.c_int,
    np.ctypeslib.ndpointer(dtype=np.uint8, ndim=1, flags="C_CONTIGUOUS"),
    ctypes.c_int,
]

lib.find_match.restype = ctypes.c_int


def find_match(dic, buf):
    l = ctypes.c_int()
    d = lib.find_match(dic, len(dic), buf, len(buf), ctypes.byref(l))
    return (d, l.value)
