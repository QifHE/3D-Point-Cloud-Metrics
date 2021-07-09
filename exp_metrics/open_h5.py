import h5py as h5
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # 用于阅读h5文件的keys
    f = h5.File("/h5文件所在的路径.h5", "r")
    print(f.keys())