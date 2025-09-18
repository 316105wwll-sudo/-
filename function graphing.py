import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_3d_function(func, x_range=(-5, 5), y_range=(-5, 5), points=100,
                     title="3D Function Plot", colormap=cm.coolwarm):
    """
    绘制三维函数图像

    参数:
    func: 要绘制的函数，形式为f(x, y)
    x_range: x轴范围，元组形式(x_min, x_max)
    y_range: y轴范围，元组形式(y_min, y_max)
    points: 每个轴上的采样点数量
    title: 图像标题
    colormap: 颜色映射
    """
    try:
        # 创建网格数据
        x = np.linspace(x_range[0], x_range[1], points)
        y = np.linspace(y_range[0], y_range[1], points)
        X, Y = np.meshgrid(x, y)

        # 计算函数值
        Z = func(X, Y)

        # 创建图形和3D坐标轴
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # 绘制3D表面
        surf = ax.plot_surface(X, Y, Z, cmap=colormap,
                               linewidth=0.5, antialiased=True,
                               alpha=0.8)

        # 添加颜色条
        fig.colorbar(surf, shrink=0.5, aspect=5)

        # 设置标题和标签
        ax.set_title(title, fontsize=15)
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.set_zlabel('Z', fontsize=12)

        # 设置视角
        ax.view_init(elev=30, azim=45)

        # 显示图像
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"绘图时发生错误: {str(e)}")


# 示例函数1: 马鞍面 (双曲抛物面)
def saddle_function(x, y):
    return x ** 2 / 10 - y ** 2 / 10


# 示例函数2:  sinc函数
def sinc_function(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    return np.sin(r) / r if np.any(r != 0) else 1.0


# 示例函数3: 高斯函数
def gaussian_function(x, y):
    return np.exp(-(x ** 2 + y ** 2) / 10)


if __name__ == "__main__":
    # 绘制马鞍面
    plot_3d_function(
        saddle_function,
        x_range=(-10, 10),
        y_range=(-10, 10),
        title="马鞍面: z = x²/10 - y²/10"
    )

    # 绘制sinc函数
    plot_3d_function(
        sinc_function,
        x_range=(-10, 10),
        y_range=(-10, 10),
        title="Sinc函数: z = sin(√(x²+y²))/√(x²+y²)",
        colormap=cm.viridis
    )

    # 绘制高斯函数
    plot_3d_function(
        gaussian_function,
        x_range=(-5, 5),
        y_range=(-5, 5),
        title="高斯函数: z = e^(-(x²+y²)/10)",
        colormap=cm.plasma
    )
