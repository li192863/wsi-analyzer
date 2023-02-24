import os

from PIL import Image
import numpy as np

# 配置环境变量
vipshome = os.path.join(os.getcwd(), 'vips-dev-8.14', 'bin')
os.environ['PATH'] = vipshome + ';' + os.environ['PATH']
import pyvips  # 导入pyvips包


class ImageSlicer(object):
    def __init__(self, slice_size, drop_last=True, enable_filter=True, threshold=230, prefix='', suffix='.jpg'):
        """
        初始化图片切割器
        :param slice_size: 切片大小 [height, width]
        :param drop_last: 舍弃图片边缘
        :param threshold: 方差阈值
        :param prefix: 文件前缀
        :param suffix: 文件后缀
        """
        self.slice_size = slice_size
        self.drop_last = drop_last
        self.enable_filter = enable_filter
        self.threshold = threshold
        self.prefix = prefix
        self.suffix = suffix

    def generate_slices(self, files):
        """
        切割多个文件
        :param files:
        :return:
        """
        # 保存图片切片
        for file in files:
            # 分割图片
            outputs = self._slice_image(file)
            # 过滤空白
            if self.enable_filter:
                outputs = self._filter_images(outputs)
            # 创建文件
            filepath, filename = os.path.split(file)
            image_name = filename.split('.')[0]
            target_dir = os.path.join(filepath, image_name)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            self._save_images(outputs, target_dir)

    def _slice_image(self, file):
        """
        分割图片为列表
        :param file:
        :return:
        """
        # 读取图片
        img = pyvips.Image.new_from_file(file, access='sequential').numpy()
        h, w, d = img.shape

        # 分割图片
        output = []
        stride_h, stride_w = self.slice_size
        for i in range(0, h, stride_h):
            for j in range(0, w, stride_w):
                end_h = i + stride_h
                end_w = j + stride_w
                # 是否舍弃多余图像
                if self.drop_last:
                    if end_h > h or end_w > w:
                        continue  # 舍弃图像
                else:
                    end_h = min(h, end_h)
                    end_w = min(w, end_w)
                output.append({"image": img[i: end_h, j: end_w, :], "row": i // stride_h, "col": j // stride_w})
                # # used for debug
                # if len(output) >= 1000:
                #     break
        return output

    def _filter_images(self, outputs):
        """
        指定阈值过滤图片
        :param outputs: 包含图片数组
        :return:
        """
        slow, fast = 0, 0
        while fast < len(outputs):
            image = outputs[fast]["image"]
            # # 基于方差
            # std_val = np.mean([np.std(image[..., 0]), np.std(image[..., 1]), np.std(image[..., 2])])
            # if std_val > self.threshold:
            #     outputs[slow] = outputs[fast]
            #     slow += 1
            # # 基于空白
            ratio = np.sum(np.mean(image, axis=-1) > self.threshold) / image.shape[0] / image.shape[1]  # [0 ~ 1]
            # ratio = compute_white_ratio(image, as_white)
            if ratio <= 0.5:
                outputs[slow] = outputs[fast]  # 过滤空白照片
                slow += 1

            fast += 1
        return outputs[:slow]

    def _save_images(self, outputs, target_dir=None):
        """
        保存图片至指定文件夹
        :param outputs:
        :param target_dir:
        :return:
        """
        # 指定文件名
        images = [output['image'] for output in outputs]
        rows = [output['row'] for output in outputs]
        cols = [output['col'] for output in outputs]
        # 获取宽度
        width = len(str(len(outputs)))  # 获取图片数量位数
        index_width = max(len(str(max(rows))), len(str(max(cols))))
        for i, image in enumerate(images):
            slice_name = self.prefix + str(i).zfill(width) + '_' + str(rows[i]).zfill(index_width) + '_' + str(
                cols[i]).zfill(index_width) + self.suffix
            img = Image.fromarray(image).convert('RGB')
            img.save(os.path.join(target_dir, slice_name))

if __name__ == '__main__':
    # options = {
    #     'slice_size': [512, 512],
    #     'filter_image': True,
    #     'threshold': 50,
    #     'prefix': '',
    #     'suffix': '.jpg'
    # }
    # files = ['../test.svs', '../test2.svs']
    files = [r"C:\Users\ChestnutLee\Desktop\TCGA-2Y-A9GW-01Z-00-DX1.71805205-933D-4D72-A4A2-586DC5490D76(1).svs"]
    slicer = ImageSlicer(slice_size=[892, 892], threshold=235)
    slicer.generate_slices(files)
