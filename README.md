# 3D-Point-Cloud-Metrics

<p float="left">
    <img src="https://user-images.githubusercontent.com/34999814/125043661-be445980-e0cd-11eb-8805-5ef5bbed76b6.png" height="250">
    <img src="https://user-images.githubusercontent.com/34999814/125043824-edf36180-e0cd-11eb-8862-1af57c0557c7.png" height="250">
    <img src="https://user-images.githubusercontent.com/34999814/125044052-2b57ef00-e0ce-11eb-8d8b-f9cec3a39fc5.png" height="250">
</p>

用于将体素和网格文件批量转换为点云，并能计算三个适用于三维点云的生成质量衡量标准Coverage (COV)，Minimum Matching Distance (MMD)，和Jensen-Shannon Divergence (JSD)。

本计算基于论文《Learning Representations and Generative Models For 3D Point Clouds》，首次应用于对《PQ-NET: A Generative Part Seq2Seq Network for 3D Shapes》中Shape Generation实验的复刻。参考了这个issue：https://github.com/ChrisWu1997/PQ-NET/issues/19

---

**Learning Representations and Generative Models For 3D Point Clouds**

Panos Achlioptas, Olga Diamanti, Ioannis Mitliagkas, Leonidas Guibas

[ArXiv](https://arxiv.org/abs/1707.02392) [GitHub](https://github.com/optas/latent_3d_points)

Citation: Achlioptas, Panos, et al. "Learning representations and generative models for 3d point clouds." *International conference on machine learning.* PMLR, 2018.

---

**PQ-NET: A Generative Part Seq2Seq Network for 3D Shapes**

Rundi Wu, Yixin Zhuang, Kai Xu, Hao Zhang, Baoquan Chen

[ArXiv](https://arxiv.org/abs/1911.10949) [GitHub](https://github.com/ChrisWu1997/PQ-NET)

Wu, Rundi, et al. "Pq-net: A generative part seq2seq network for 3d shapes." *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.* 2020.

---

## 环境

对体素和网格文件的处理不需要特别的环境，只需要Python 3.x和Anaconda 3

在得到点云文件后需要单独创建一个虚拟环境适用于lantent_3d_points，满足

 - Python 2.7+ with Numpy, Scipy and Matplotlib
 - Tensorflow (version 1.0+)
 - TFLearn==0.3.2
 - CUDA = 8.0 or 9.0 (10.0未进行过测试)

在2021年后的pip无法直接安装python 2.7，可以使用命令
```
conda create --override-channels -c defaults -n py27 python=2.7
```
创建一个使用python 2.7名为py27的虚拟环境

## 安装

计算衡量标准部分将直接在lantent_3d_points的代码上进行修改，需要latent_3d_points的完整库：
```
git clone https://github.com/optas/latent_3d_points.git
```
需要根据lantent_3d_points进行其他安装步骤，其中/latent_3d_points/external/structural_losses/makefile的修改需要根据实际CUDA版本、路径以及tensorflow库路径等进行修改，参考这个issue：https://github.com/optas/latent_3d_points/issues/21

下载需要使用的代码：
```
git clone https://github.com/Mistral-Twirl/3D-Point-Cloud-Metrics.git
```
将/3D-Point-Cloud-Metrics/exp_metrics/compute_evaluation_metrics.py文件移动到/latent_3d_points/notebooks/路径下：
```
mv 根目录/3D-Point-Cloud-Metrics/exp_metrics/compute_evaluation_metrics.py 根目录/latent_3d_points/notebooks
```
## 文件处理

1. 读取h5文件的keys：
需要在代码中指定h5路径
```
cd 根目录/3D-Point-Cloud-Metrics/exp_metrics/
python open_h5.py
```

2. 基于JSON文件的数据集分割：
可以从完整数据集中分割出测试集，需要在代码中指定文件和文件夹路径
```
cd 根目录/3D-Point-Cloud-Metrics/exp_metrics/
python dataset_split.py
```
3. h5体素文件批量转换为obj网格文件：
需要指定h5文件要提取的key和文件夹路径
```
cd 根目录/3D-Point-Cloud-Metrics/exp_metrics/
python voxel2mesh_from_h5_batch.py
```
4. obj网格文件批量转换为ply点云文件：
需要指定文件夹路径和文件名
```
cd 根目录/3D-Point-Cloud-Metrics/exp_metrics/
python mesh2pc_batch.py
```
5. 处理latent_3d_points数据储存：
```
cd 根目录/3D-Point-Cloud-Metrics/
mkdir data
cd data
mkdir shape_net_core_uniform_samples_2048
```
在上面那个文件夹下根据/latent_3d_points/src/in_out.py文件里给出的category id随意创建两个以id为名的文件夹，一个储存生成点云文件，一个储存真实点云文件
```
mkdir .......
mkdir .......
```

6. 移动数据到latent_3d_points：
需要自己修改代码中的路径
```
cd 根目录/3D-Point-Cloud-Metrics/exp_metrics/
sh move_files.sh
```
7. 计算衡量标准：
将所有点云文件归一化到半径为一的单位立体球中，然后计算COV、MMD、JSD。需要修改代码中的一些路径和文件名
```
conda activate py27
cd 根目录/latent_3d_points/notebooks/
python compute_evaluation_metrics.py
```
## 其他文件
visualization_h5_batch.py
可以批量可视化h5体素文件，基于https://github.com/ChrisWu1997/PQ-NET/issues/7 修改
mesh2pc_batch_normalized.py
在把体素转换成点云的同时进行归一化
