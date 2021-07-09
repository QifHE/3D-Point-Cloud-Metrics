import numpy as np
import os.path as osp
import sys
sys.path.append("..")                           # 根据latent3D路径设置

from src.evaluation_metrics import minimum_mathing_distance, \
jsd_between_point_cloud_sets, coverage

from src.in_out import snc_category_to_synth_id,\
                                        load_all_point_clouds_under_folder

def scale_to_half_unit_sphere(points, center=None):         # 标准化为0.5半径的球
    midpoints = np.mean(points, axis=0)
    points = points - midpoints
    scale = np.max(np.sqrt(np.sum(points ** 2, axis=1)))
    points = points / (scale * 2)
    return points

def scale_to_unit_sphere(points, center=None):          # 标准化为1半径的球
    midpoints = (np.max(points, axis=0) + np.min(points, axis=0)) / 2
    points = points - midpoints
    scale = np.max(np.sqrt(np.sum(points ** 2, axis=1)))
    points = points / scale
    return points

top_in_dir = "/........./latent_3d_points/data/shape_net_core_uniform_samples_2048/" # Top-dir of where point-clouds are stored.
#class_name = raw_input('Give me the class name (e.g. "chair"): ').lower()
#class_name_re = raw_input('Give me the class name (e.g. "chair"): ').lower()
class_name = "..."          # 生成的点云使用的文件夹对应的类别名，参考/src/in_out.py
class_name_re = "..."      # 真实的点云使用的文件夹对应的类别名，参考/src/in_out.py

syn_id = snc_category_to_synth_id()[class_name]
syn_id_re = snc_category_to_synth_id()[class_name_re]

class_dir = osp.join(top_in_dir , syn_id)
class_dir_re = osp.join(top_in_dir , syn_id_re)

all_pc_data = load_all_point_clouds_under_folder(class_dir, n_threads=8, file_ending='.ply', verbose=True)
all_pc_data_re = load_all_point_clouds_under_folder(class_dir_re, n_threads=8, file_ending='.ply', verbose=True)

n_ref = ...... # size of ref_pcs.
n_sam = ...... # size of sample_pcs.
all_ids_re = np.arange(all_pc_data_re.num_examples)
all_ids = np.arange(all_pc_data.num_examples)

ref_ids = np.random.choice(all_ids_re, n_ref, replace=False)
sam_ids = np.random.choice(all_ids, n_sam, replace=False)

ref_pcs = all_pc_data_re.point_clouds[ref_ids]
sample_pcs = all_pc_data.point_clouds[sam_ids]

for i in range(n_ref):
    ref_pcs[i] = scale_to_unit_sphere(ref_pcs[i], center=None)
for i in range(n_sam):
    sample_pcs[i] = scale_to_unit_sphere(sample_pcs[i], center=None)

ae_loss = 'chamfer'  # Which distance to use for the matchings.
#ae_loss='emd'
if ae_loss == 'emd':
    use_EMD = True
else:
    use_EMD = False  # Will use Chamfer instead.

batch_size = 32     # Find appropriate number that fits in GPU.
normalize = True     # Matched distances are divided by the number of 
                     # points of thepoint-clouds.

mmd, matched_dists = minimum_mathing_distance(sample_pcs, ref_pcs, batch_size, normalize=normalize, use_EMD=use_EMD)

cov, matched_ids = coverage(sample_pcs, ref_pcs, batch_size, normalize=normalize, use_EMD=use_EMD)

jsd = jsd_between_point_cloud_sets(sample_pcs, ref_pcs, resolution=28)

print("To be, or not to be, that is the question:")
print("COV " + str(100 * cov))
print("MMD " + str(1000 * mmd))
print("JSD " + str(jsd))

# Open file for writing
fileObject = open("/...............txt", "w")       #保存实验结果到txt文件
# Add some text
fileObject.write("COV " + str(100 * cov) + "\n")
fileObject.write("MMD " + str(1000 * mmd) + "\n")
fileObject.write("JSD " + str(jsd))

# Close the file
fileObject.close()