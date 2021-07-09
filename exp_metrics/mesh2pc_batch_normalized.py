import os
import sys
import numpy as np
import trimesh
from plyfile import PlyData, PlyElement
#from eulerangles import euler2mat
import fnmatch          # match h5 files
from rich.progress import track # pip install rich

base_path = "/网格文件所在文件夹/"
save_path = "/点云文件保存文件夹/"

sample_num = 2000                  # number of sampled points 


def write_ply(points, filename, text=True):
     """ input: Nx3, write points to filename as PLY format. """
     points = [(points[i,0], points[i,1], points[i,2]) for i in range(points.shape[0])]
     vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4')])
     el = PlyElement.describe(vertex, 'vertex', comments=['vertices'])
     PlyData([el], text=text).write(filename)

def scale_to_unit_sphere(points, center=None):                  # 标准化为半径为1的单位球
    midpoints = (np.max(points, axis=0) + np.min(points, axis=0)) / 2
#    midpoints = np.mean(points, axis=0)
    points = points - midpoints
    scale = np.max(np.sqrt(np.sum(points ** 2, axis=1)))
#    points = points / (scale * 2)
    points = points / scale
    return points


if __name__ == '__main__':
    listdir = fnmatch.filter(sorted(os.listdir(base_path)),'*.obj')   # load only obj mesh files

    for i in track(range(len(listdir))):        # iterate through all files and track progress
        obj_path = base_path + listdir[i]     # load one obj5 file
        mesh_file = trimesh.load(obj_path)

        pc_file = trimesh.sample.sample_surface(mesh_file, sample_num)[0]
        pc_file = scale_to_unit_sphere(pc_file, center=None)

        #pc_filename =  "ref_" + str(i).zfill(4) + ".ply"    # 点云文件名字
        pc_filename =  "sam_" + str(i).zfill(4) + ".ply"    # 点云文件名字
        write_ply(pc_file, save_path + pc_filename)  
        print(str(i) + "/" + str(len(listdir)) + " converted to point cloud")
    
    
