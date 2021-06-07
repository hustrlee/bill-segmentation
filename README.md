# 医疗票据分割

使用 OpenCV-Python 实现医疗票据分割服务。

本项目记录了所有开发步骤。



## 开发环境

1. 使用 `vscode` 作为源代码编辑器。
2. 安装 `Python <ms-python.python>`、`Pylance <ms-python.vscode-pylance>` 插件，构建 Python 开发环境。
3. 使用 Anaconda 作为 Python 的发行版本。
4. 创建 `ipt` 开发环境，并切换到该环境。

```sh
conda create --name seg python=3
source activate seg
```

5. 安装 `opencv`

```sh
pip install opencv-python -i https://pypi.mirrors.ustc.edu.cn/simple
```

> - `Pylance` 只能对 `opencv-python` 包进行代码自动补全。其它的包名称，例如：`opencv` 等，均不能进行代码补全。因此，没有使用 `conda` 安装 `opencv`，而使用 `pip` 安装 `opencv-python`。
> - `-i https://pypi.mirrors.ustc.edu.cn/simple` 指定使用“中科大”镜像源进行安装。

6. 校验 `opencv` 安装。在 `python` 命令行环境下输入：

```python
import cv2
print(cv2.__version__) # 查看 opencv 版本
```

7. 客户端使用 `Vue` 进行开发。



## 测试

### 运行服务端

```sh
cd server
source activate seg # 激活 Python 运行环境。Windows 下使用 conda activate seg
pip install -r requirement.txt # 安装依赖
python -m bill_segmentation
```



### 运行客户端

```sh
cd client
npm install # 安装依赖
npm run serve
```



## 中文路径问题

Python 采用 utf-8 编码，而 Windows 采用 Unicode 编码。而分割后的文件名中包含中文，在 Windows 下被识别为乱码，导致 Client 端不能正常显示。
