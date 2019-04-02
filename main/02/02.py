import random
import math
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np

def find_position(img, size_x, size_y):
    # 计算积分图，cumsum([1,2,3,4]) => [1,3,6,10]
    integral = np.cumsum(np.cumsum(np.asarray(img), axis=1), axis=0)

    # 使用 wordcloud 的布局策略
    for x in range(1, 800 - size_x):
        for y in range(1, 600 - size_y):
            # 检测矩形区域内容是否为空
            area = integral[y - 1, x - 1] + integral[y + size_y - 1, x + size_x - 1]
            area -= integral[y - 1, x + size_x - 1] + integral[y + size_y - 1, x - 1]
            if not area:
                return x, y

    return None, None


if __name__ == '__main__':
    words = ['发展', '中国', '人民', '建设', '社会主义', '坚持', '党', '全面', '国家', '实现', '制度', '推进', '特色', '社会']

    # 创建一张 800×600 的图片
    img = Image.new("L", (800, 600))
    draw = ImageDraw.Draw(img)

    for word in words:
        # 选择字体和大小：黑体，大小随机
        font_size = random.randint(50, 150)
        font = ImageFont.truetype('C:\Windows\Fonts\SIMHEI.TTF', font_size)

        # 计算文字矩形框的大小
        box_size = draw.textsize(word, font=font)

        # 在图片中寻找一个能放下矩形框的位置
        x, y = find_position(img, box_size[0], box_size[1])
        if x:
            # 找到一个位置，并绘制上文字
            draw.text((x, y), word, fill="white", font=font)
    img.show()
