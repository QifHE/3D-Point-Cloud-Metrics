import os
import sys
import numpy as np
import trimesh
from plyfile import PlyData, PlyElement
#from eulerangles import euler2mat
import fnmatch          # match h5 files
from rich.progress import track # pip install rich


base_path = "/.../" # directary containing obj files
save_path = "/.../"  # directary for pc files
sample_num = 2000                  # number of sampled points 


def write_ply(points, filename, text=True):
     """ input: Nx3, write points to filename as PLY format. """
     points = [(points[i,0], points[i,1], points[i,2]) for i in range(points.shape[0])]
     vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4')])
     el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
     PlyData([el], text=text).write(filename)

if __name__ == '__main__':
    listdir = fnmatch.filter(sorted(os.listdir(base_path)),'*.obj')               # load only obj mesh files

    for i in track(range(len(listdir))):                            # iterate through all files and track progress
        obj_path = base_path + listdir[i]                         # load one obj5 file
        mesh_file = trimesh.load(obj_path)
        pc_file = trimesh.sample.sample_surface(mesh_file, sample_num)[0]         # 对网格采样为点云
        #pc_filename =  "ref_" + str(i).zfill(4) + ".ply"               # 点云文件名字
        pc_filename =  "sam_" + str(i).zfill(4) + ".ply"                # 点云文件名字
        write_ply(pc_file, save_path + pc_filename)                     # 写入ply文件
        print(str(i) + "/" + str(len(listdir)) + " converted to point cloud")
    
    
