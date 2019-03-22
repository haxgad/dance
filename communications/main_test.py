import numpy as np
import itertools
from multiprocessing import Pool #  Process pool
from multiprocessing import sharedctypes

size = 100
block_size = 4

X = np.random.random((size, size))
result = np.ctypeslib.as_ctypes(np.zeros((size, size)))
shared_array = sharedctypes.RawArray(result._type_, result)


def fill_per_window(args):
    window_x, window_y = args
    tmp = np.ctypeslib.as_array(shared_array)

    for idx_x in range(window_x, window_x + block_size):
        for idx_y in range(window_y, window_y + block_size):
            tmp[idx_x, idx_y] = X[idx_x, idx_y]


if __name__ == "__main__":
    window_idxs = [(i, j) for i, j in
                   itertools.product(range(0, size, block_size),
                                     range(0, size, block_size))]

    p = Pool()
    res = p.map(fill_per_window, window_idxs)
    result = np.ctypeslib.as_array(shared_array)
    
    print(np.array_equal(X, result))
