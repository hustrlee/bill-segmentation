# 图像透视变换

使用 OpenCV-Python 实现图像的透视变换，来对拍照的文档进行矫正。本项目记录了所有开发步骤。



## 开发环境

1. 使用 Anaconda 作为 Python 开发环境。
2. 创建 `ipt` 开发环境，并切换到该环境。

```sh
conda create --name ipt python=3
conda activate ipt
```

3. 安装 `opencv`

```sh
conda install -c conda-forge opencv # main channel 中 opencv 尚未更新到 v4；conda-forge channel 中 opencv 为最新版本
```

4. 校验 `opencv` 安装。在 `python` 命令行环境下输入：

```python
import cv2
print(cv2.__version__) # 查看 opencv 版本
```

