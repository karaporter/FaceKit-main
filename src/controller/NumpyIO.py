import numpy as np



def readFile(dir, mode = 'rb'):
    with open(dir, mode) as f:
        matrix = np.load(f)

    return matrix
