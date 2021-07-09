# 用于批量可视化体素h5文件

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib.colors import LightSource
import seaborn as sns       # pip install seaborn
import h5py
import os               # loading h5 files
import fnmatch
from rich.progress import track # 一个漂亮的进度条   # 需要pip install rich

base_path = "/h5文件所在的文件夹/"
save_path = "/保存PNG图片的文件夹/"

def visualize_ndvoxel(voxel, filename):     # 修改自https://github.com/ChrisWu1997/PQ-NET/issues/7#issuecomment-788223539
    """
    :param voxel:like (64,64,64) ndarray
    :return:
    """
    voxel = np.squeeze(voxel)
    if len(voxel.shape) == 4:
        voxel = voxel[0]

    color_num = voxel.max()
    current_palette = sns.color_palette(as_cmap=True)
    colors = np.empty(voxel.shape, dtype=object)
    for i in range(color_num):
        colors[voxel == i + 1] = current_palette[i]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_axis_off()
    ax.voxels(voxel, facecolors=colors, lightsource=LightSource(azdeg=315, altdeg=45))
    # ax.set(xlabel='x', ylabel='y', zlabel='z')
    if filename:
        plt.savefig(fname=filename)
    else:
        pass
    plt.close()

# main function
listdir = fnmatch.filter(sorted(os.listdir(base_path)),'*.h5')      # load only h5 files
for i in track(range(len(listdir))):                  # iterate through all files and track progress
    h5_path = base_path + listdir[i]                # load one h5 file
    filename = save_path + str(i).zfill(4) + ".png"       # h5 文件名
    with h5py.File(h5_path, 'r') as fp:
        voxel = fp['voxel'][:]

    visualize_ndvoxel(voxel,filename)
    print(str(i) + "/" + str(len(listdir)) + " visualized")