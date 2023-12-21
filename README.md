# 切片分析系统

## 项目介绍

本项目为切片分析系统，可对医学图像当中的病理切片进行处理，并进行推理和分析。

该程序实现功能为：将一张或多张病理切片，输出各个切片的病理分析报告。

### 下载

1. 下载源码。

```
git clone https://github.com/li192863/wsi-analyzer.git
```

2. 下载`vips-dev-8.14`，将其解压放置于`./wsi-analyzer`文件夹下，下载地址在[这里](https://github.com/libvips/build-win64-mxe/releases/tag/v8.14.5)。如果需要更换版本，请修改`./utils/size_util.py`。

```shell
vipshome = os.path.join(os.getcwd(), 'path/to/vips', 'bin')
```

3. 放置权重，权重文件分别为`./weights/seg_model.pth`和`./weights/cla_model.pth`。
4. 修改模型，更改`model`文件夹下的模型文件，并更改`./model/model.py`中的`get_seg_model`与`get_cla_model`函数。
5. 修改配置，更改`./conf/settings.yml`中有关于`inferencer`的相关配置。
6. 运行`./main.py`。

### 运行

打开软件，软件首先加载默认配置，随后根据默认配置（`./conf/settings.yml`）生成当前运行配置（`./conf/running_set.yml`）。

选择文件，只可选择一个文件夹下的一个或多个文件，选择后如果再次点击选择文件，原有文件列表将被清空。

开始转换，软件将对病理切片进行切片处理，生成分割切片与分类切片，随后将对分割/分类切片进行推理，并将推理结果进行融合结果分析，最后生成报告文件，保存在目标文件夹下。

注意，界面配置始终优于运行配置。例如文件列表等，直接修改配置文件中文件列表选项将不起作用。

### 配置

配置文件为`./conf/settings.yml`，配置可根据需要自行更改。

```yml
# 默认配置文件（请以utf-8编码打开此文件）

# Default config file (please open with utf-8)


# 修改配置时注意遵循YAML格式规范：
#    所有符号均为半角符号（:, ', ", (, ), [, ], {, }, ...），
#    在冒号后必须有一个空格

# Please follow the yaml format while editing this file:
#    all symbols should be half-width (:, ', ", (, ), [, ], {, }, ...),
#    there must be a space after a colon.


# 基础配置
basic:
  # 文件列表
  filelist: []
  # 尝试自动恢复 填 True, False
  auto_resume: True
  # 强制重新推理（无论之前推理是否完成，仍进行推理） 填 True, False
  force_inference: False
  # 输出地址 填 null(自动选择), '/path/to/result'
  result_folder: ''

# 切片配置
slicer:
  # 分割相关配置
  segmentation:
    # 切片大小 [width, height]
    slice_size: [2048, 2048]
    # 降采样值
    down_sample: 16
    # 文件前缀（不得包含特殊字符）
    prefix: ''
    # 文件后缀（默认文件格式，除'.'外不得包含特殊字符） 填'.jpg', '.png' 等
    suffix: '.jpg'
    # 是否采用内存加载（内存加载速度较快，但可能会导致内存溢出） 填 True, False
    memory: True
  # 分类相关配置
  classification:
    # 切片大小 [width, height]
    slice_size: [1024, 1024]
    # 降采样值
    down_sample: 1
    # 文件前缀
    prefix: ''
    # 文件后缀（默认文件格式） 填'.jpg', '.png' 等
    suffix: '.jpg'
    # 是否采用内存加载（内存加载速度较快，但可能会导致内存溢出） 填 True, False
    memory: True
  # 切片器引擎 填 'base', 'vips'
  engine: 'vips'
  # 默认是否舍弃边缘 填 True, False
  drop_last: False

# 推理配置
inferencer:
  # 分割相关配置
  segmentation:
    # 推理时使用的权重
    weight: './weights/seg_model.pth'
    # 推理的种类
    classes: ['背景', '正常', '肿瘤']
    # 推理变形后大小 **[height, width]**
    inference_size: [1024, 1024]
    # 推理时批次的大小（值越大推理越快，但可能导致显存溢出） 填 2, 1
    batch_size: 2
    # 推理时使用的设备 填 null(自动选择), 'cuda', 'cpu'
    device: 'cpu'
  # 分类相关配置
  classification:
    # 推理时使用的权重
    weight: './weights/cla_model.pth'
    # 推理的种类
    classes: ['出血', '坏死', '实质', '淋巴', '空泡', '空白', '间质']
    # 推理变形后大小 **[height, width]**
    inference_size: [256, 256]
    # 推理时批次的大小（值越大推理越快，但可能导致显存溢出） 填 32, 16, 8, 4, 2, 1
    batch_size: 16
    # 推理时使用的设备 填 null(自动选择), 'cuda', 'cpu'
    device: 'cpu'

# 结果配置
result:
  # 分割相关配置
  segmentation:
    # 除去前后缀外切片命名格式
    naming_regex: 'd(\d+)_r(\d+)_c(\d+)'
    # 输出图形选项
    summary_image:
      # 是否显示图片
      show_image: False
      # 图片选项
      plot_kwargs:
        # 颜色映射，详见 https://matplotlib.org/stable/users/explain/colors/colormaps.html
        cmap: 'plasma'
      # 保存选项
      save_kwargs:
        # 分辨率dpi(dots per inch)
        dpi: 1024
  # 分类相关配置
  classification:
    # 除去前后缀外切片命名格式
    naming_regex: 'd(\d+)_r(\d+)_c(\d+)'
    # 输出图形选项
    summary_image:
      # 是否显示图片
      show_image: False
      # 图片选项
      plot_kwargs:
        # 颜色映射，详见 https://matplotlib.org/stable/users/explain/colors/colormaps.html
        cmap: 'viridis'
      # 保存选项
      save_kwargs:
        # 分辨率dpi(dots per inch)
        dpi: 1024
```