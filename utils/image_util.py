import matplotlib
import matplotlib.pyplot as plt

plt.style.use('_mpl-gallery-nogrid')
matplotlib.use('QtAgg')


def write_image(tensor, save_path=None, show_image=False, plot_kwargs=dict(), save_kwargs=dict()):
    """
    可视化一个二维矩阵
    :param tensor: 输入的二维矩阵
    :param cmap: 颜色映射
    :return: 图片
    """
    fig, ax = plt.subplots()
    ax.imshow(tensor, **plot_kwargs)
    ax.axis('off')  # 关闭坐标轴
    # fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    if save_path is not None:
        fig.savefig(save_path, **save_kwargs)
    if show_image:
        plt.show()


def write_contour(tensor, save_path=None, show_image=False, plot_kwargs=dict(), save_kwargs=dict()):
    """
    可视化一个二维矩阵
    :param tensor: 输入的二维矩阵
    :param cmap: 颜色映射
    :return: 图片
    """
    fig, ax = plt.subplots()
    ax.contourf(tensor, **plot_kwargs)
    ax.axis('off')  # 关闭坐标轴
    if save_path is not None:
        fig.savefig(save_path, **save_kwargs)
    if show_image:
        plt.show()


if __name__ == '__main__':
    import torch
    random_tensor = torch.rand(5, 5)
    write_image(random_tensor, save_path='./test.png')
    write_contour(random_tensor, save_path='./test.png')