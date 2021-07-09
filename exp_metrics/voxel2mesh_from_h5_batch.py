import os
import sys
import numpy as np
import mcubes           # marching cubes
import h5py as h5
import fnmatch          # match h5 files
from rich.progress import track # pip install rich

base_path = "/home/heqifeng/PQ-NET/proj_log/pqnet-PartNet-Lamp/results/rec-ckpt-1000-voxel-p0/"
save_path = "/home/heqifeng/PQ-NET/exp_pc/Lamp_files/Lamp_GAN_mesh_files/"

def h5toNpArray(path):
    with h5.File(path, "r") as h5File:
        #npArray = h5File['shape_voxel64'][()]
        npArray = h5File['voxel'][()]
    return npArray

if __name__ == '__main__':
    listdir = fnmatch.filter(sorted(os.listdir(base_path)),'*.h5')   # load only h5 files
    
    for i in track(range(len(listdir))):        # iterate through all files and track progress
        h5_path = base_path + listdir[i]     # load one h5 file
        #print(h5_path)
        matrix = h5toNpArray(h5_path)       # load np arrays

        vertices, triangles = mcubes.marching_cubes(matrix,0)
        #mcubes.export_mesh(vertices, triangles, "sphere.dae", "MySphere")
        mesh_filename = str(i).zfill(4) + ".obj"        
        mcubes.export_obj(vertices, triangles, save_path + mesh_filename)
        print(str(i) + "/" + str(len(listdir)) + " converted to mesh")