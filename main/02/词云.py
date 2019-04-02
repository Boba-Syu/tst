# -*- coding: utf-8 -*-
import numpy as np
import random
import math

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor


class Region:
    size = 50
    height = 0
    width = 0

    def __init__(self, width, height, size):
        self.regions = {}
        self.size = size

    def add_sprite(self, sprite, x, y):
        width = sprite.img.size[0]
        height = sprite.img.size[1]
        from_x = (x // self.size)
        from_y = (y // self.size)
        to_x = ((x + width) // self.size)
        to_y = ((y + height) // self.size)
        for i in range(from_x, to_x + 1):
            for j in range(from_y, to_y + 1):
                key = '{}-{}'.format(i, j)
                if not key in self.regions:
                    self.regions[key] = []
                self.regions[key].append(sprite)

    def check_sprite(self, sprite, x, y):
        width = sprite.img.size[0]
        height = sprite.img.size[1]
        from_x = (x // self.size)
        from_y = (y // self.size)
        to_x = ((x + width) // self.size)
        to_y = ((y + height) // self.size)
        region_need_to_check = []
        for i in range(from_x, to_x + 1):
            for j in range(from_y, to_y + 1):
                key = '{}-{}'.format(i, j)
                if key in self.regions:
                    region_need_to_check = list(set(region_need_to_check + self.regions[key]))
        return region_need_to_check


class QuadTree:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    width = 0
    height = 0
    children = None

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2


class Sprite:
    text = ''
    rotate = 0
    x = None
    y = None
    tree = None
    font_size = None
    img = None

    def build_tree(self):
        integral = np.cumsum(np.cumsum(np.asarray(self.img), axis=1), axis=0)
        width = self.img.size[0]
        height = self.img.size[1]

        self.tree = self._build_tree(integral, 1, 1, width - 2, height - 2)

    def _build_tree(self, integral, x1, y1, x2, y2):
        area = integral[y1 - 1, x1 - 1] + integral[y2, x2]
        area -= integral[y1 - 1, x2] + integral[y2, x1 - 1]
        if not area:
            # 区域内没有像素
            return None

        # 区域内有像素，继续划分
        children = []
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)

        tree = QuadTree(x1, y1, x2, y2)

        # 四叉树最小矩形边长, 该值越大, 速度越快, 但结果越不精确
        min_rect_size = 2
        if x2 - x1 > min_rect_size or y2 - y1 > min_rect_size:
            c0 = self._build_tree(integral, x1, y1, cx, cy)
            c1 = self._build_tree(integral, cx, y1, x2, cy)
            c2 = self._build_tree(integral, x1, cy, cx, y2)
            c3 = self._build_tree(integral, cx, cy, x2, y2)
            if c0:
                children.append(c0)
            if c1:
                children.append(c1)
            if c2:
                children.append(c2)
            if c3:
                children.append(c3)
            if len(children):
                tree.children = children
        return tree


# 矩形重叠检测
def rect_collide(a, b, x1, y1, x2, y2):
    return y1 + a.y2 > y2 + b.y1 and y1 + a.y1 < y2 + b.y2 and x1 + a.x2 > x2 + b.x1 and x1 + a.x1 < x2 + b.x2


# 四叉树重叠检测
def overlaps(tree, other_tree, x1, y1, x2, y2):
    if rect_collide(tree, other_tree, x1, y1, x2, y2):
        if not tree.children:
            if not other_tree.children:
                return True
            else:
                for i in range(0, len(other_tree.children)):
                    if overlaps(tree, other_tree.children[i], x1, y1, x2, y2):
                        return True

        else:
            for i in range(0, len(tree.children)):
                if overlaps(other_tree, tree.children[i], x2, y2, x1, y1):
                    return True

    return False


# [布局] 阿基米德螺线
def archimedean_spiral(width, height):
    def sprial(t, offset=0):
        t = offset + t / 5
        x = int(t * math.cos(t) + (width) // 2)
        y = int(t * math.sin(t) + (height) // 2)
        return x, y, t

    return sprial


# [布局] 矩形螺线
def rectangular_sprial(width, height):
    # 螺旋步长, 该值越大, 速度越快, 但结果越不精确
    dy = dx = 10
    x = y = 0

    def sprial(t, offset=0):
        t = t + offset
        nonlocal x, y
        sign = -1 if t < 0 else 1
        num = int(math.sqrt(1 + 4 * sign * t) - sign) & 3
        if num == 0:
            x += dx
        elif num == 1:
            y += dy
        elif num == 2:
            x -= dx
        else:
            y -= dy
        return x + (width) // 2, y + (height) // 2, t

    return sprial


def find_position(sprite, bounds, offset=0):
    global width, height
    dt = 0
    sprial = rectangular_sprial(width, height)
    i = 0
    while True:
        dt += 1
        x, y, ret = sprial(dt, offset)
        if x > width - sprite.img.size[0] or x < 0 or y > height - sprite.img.size[1] or y < 0:
            break

        placed = bounds.check_sprite(sprite, x, y)
        ok = True
        i += len(placed)

        for p in placed:
            if overlaps(sprite.tree, p.tree, x, y, p.x, p.y):
                ok = False
                break
        if ok:
            return x, y, ret
    return None, None, None

if __name__ == '__main__':

    # 词语列表
    words = [('发展', 500), ('中国', 169), ('人民', 157), ('建设', 148), ('社会主义', 147), ('坚持', 131), ('党', 104), ('全面', 90),
             ('国家', 90), ('实现', 83), ('制度', 83), ('推进', 81), ('特色', 80), ('社会', 80), ('政治', 80), ('新', 78), ('加强', 71),
             ('体系', 68), ('文化', 66), ('时代', 64), ('我们', 64), ('必须', 61), ('经济', 59), ('伟大', 58), ('完善', 51), ('我国', 50),
             ('现代化', 47), ('推动', 47), ('安全', 46), ('创新', 44), ('更加', 44), ('民主', 44), ('中华民族', 43), ('改革', 43),
             ('工作', 42),
             ('增强', 39), ('不断', 37), ('战略', 36), ('治理', 36), ('领导', 36), ('问题', 35), ('加快', 35), ('深化', 35), ('对', 34),
             ('世界', 34), ('中', 34), ('文明', 33), ('复兴', 32), ('坚决', 32), ('提高', 32), ('生态', 32), ('基本', 31), ('法治', 31),
             ('教育', 31), ('思想', 30), ('生活', 30), ('民族', 30), ('重大', 27), ('能力', 27), ('统一', 27), ('促进', 27), ('历史', 27),
             ('更', 27), ('全党', 25), ('构建', 25), ('群众', 25), ('健全', 24), ('国际', 24), ('维护', 24), ('保障', 24), ('建成', 23),
             ('二', 23), ('形成', 23), ('人类', 23), ('解决', 23), ('团结', 22), ('监督', 22), ('理论', 22), ('斗争', 22), ('实践', 22),
             ('事业', 21), ('从', 21), ('机制', 21), ('协商', 21), ('保护', 21), ('组织', 21), ('政策', 21), ('统筹', 20), ('实施', 20),
             ('体制', 20), ('党内', 20), ('合作', 20), ('一个', 20), (' 要求', 20), ('基础', 20), ('支持', 20), ('贯彻', 19),
             ('依法治国', 19),
             ('强国', 19), ('创造', 19), ('共同', 19), ('强 化', 19), ('中国共产党', 18), ('重要', 18), ('奋斗', 18), ('精神', 18),
             ('政府', 18),
             ('方式', 18), ('建立', 18), ('反 对', 18), ('干部', 18), ('全体', 18), ('小康社会', 17), ('同志', 17), ('们', 17),
             ('保持', 17),
             ('全', 17), ('军队', 17), ('力量', 17), ('道路', 17), ('让', 17), ('始终', 16), ('根本', 16), ('成为', 16), ('有效', 16),
             ('和平', 16), ('作用', 16), ('梦', 15), ('方面', 15), ('党的领导', 15), ('巩固', 15), ('科学', 15), ('绿色', 15),
             ('坚定', 15),
             ('香港', 15), ('美好生活', 14), ('党和国家', 14), ('取得', 14), ('来', 14), ('协调', 14), ('深入', 14), ('积极', 14),
             ('开展', 14),
             ('持续', 14), ('自信', 14), ('稳定', 14), ('农村', 14), ('国防', 14), ('澳门', 14), ('原则', 14), ('强大', 14),
             ('保 证', 14),
             ('自觉', 14), ('确保', 14), ('发挥', 14), ('理念', 13), ('主体', 13), ('水平', 13), ('马克思主义', 13), ('管 理', 13),
             ('就业', 13),
             ('强军', 13), ('命运', 13), ('党的建设', 13), ('走', 13), ('和谐', 13), ('梦想', 13), ('革命', 13), ('利益', 13),
             ('开放', 13),
             ('基层', 13), ('○', 13), ('作为', 12), ('带领', 12), ('全国', 12), ('质量', 12), ('农业', 12), ('繁荣', 12), ('扩大', 12),
             ('健康', 12), ('全球', 12), ('军事', 12), ('人民军队', 12), ('意识', 12), ('突出', 12), ('长期', 12), ('没有', 12),
             ('将', 12),
             ('进行', 12), ('本领', 12), ('依法', 12), ('深刻', 11), ('变化', 11), ('勇于', 11), ('变革', 11), ('当家作主', 11),
             ('广泛', 11),
             ('全民', 11), ('体制改革', 11), ('核心', 11), ('两岸', 11), ('具有', 11), ('面临', 11), ('民生', 11), ('各国', 11),
             ('关系', 11),
             ('各种', 11), ('引领', 11), ('培育', 11), ('生产', 11), ('现代', 11), ('政党', 11), ('进入', 10), ('继续', 10),
             ('各族人民', 10),
             ('提升', 10), ('优化', 10), ('领域', 10), ('活力', 10), ('弘扬', 10), ('脱贫', 10), ('收入', 10), ('环境', 10),
             ('一国两制', 10),
             ('中央', 10), ('纪律', 10), ('执政', 10), ('矛盾', 10), ('科技', 10), ('明确', 10), ('服务', 10), ('注重', 10), ('人才', 10),
             ('产业', 10), ('夺取', 9), ('阶段', 9), ('使命', 9), ('这个', 9), ('一定', 9), ('与', 9), ('五年', 9), ('总', 9),
             ('改革开放', 9),
             ('党中央', 9), ('五', 9), ('作出', 9), ('区域', 9), ('着力', 9), ('权力', 9), ('传统', 9), ('实力', 9), ('覆盖', 9),
             ('牢牢', 9),
             ('活动', 9), ('坚强', 9), ('目标', 9), ('担当', 9), ('提出', 9), ('提供', 9), ('需要', 9), ('落实', 9), ('同胞', 9),
             ('认识', 9),
             ('结合', 9), ('方向', 9), ('新型', 9), ('参与', 9), ('树立', 9), ('重点', 9), ('培养', 9), ('党员', 9), ('决胜', 8),
             ('奋斗目标', 8),
             ('以来', 8), ('机构', 8), ('坚定不移', 8), ('有机', 8), ('意识形态', 8), ('地位', 8), ('价 值观', 8), ('改善', 8), ('引导', 8),
             ('格局', 8), ('宪法', 8), ('分裂', 8), ('共同体', 8), ('力', 8), ('做', 8), ('风险', 8), ('考验', 8), ('充分', 8),
             ('城乡', 8),
             ('日益增长', 8), ('更好', 8), ('美丽', 8), ('进步', 8), ('祖国', 8), ('三', 8), ('行动', 8), ('四', 8), ('融合', 8),
             ('自然', 8),
             ('自我', 8), ('人大', 8), ('主题', 7), ('激励', 7), ('复杂', 7), ('挑战', 7), ('历史性', 7), ('从严治党', 7), ('布局', 7),
             ('增长', 7), ('供给', 7), ('成果', 7), ('立法', 7), ('指导', 7), ('显著', 7), ('全党全国', 7), ('应对', 7), ('赋予', 7),
             ('大国', 7),
             ('条件', 7), ('倡导', 7), ('权威', 7), ('标准', 7), ('最大', 7), ('反腐败', 7), ('不能', 7), ('平衡', 7), ('强', 7),
             ('努力', 7),
             ('起来', 7), ('正确', 7), ('党和人民', 7), ('作风', 7), ('各项', 7), ('共享', 7), ('市场', 7), ('形式', 7), ('生态环境', 7),
             ('两个', 7), ('善于', 7), ('企业', 7), ('导向', 7), ('青年', 7), ('职责', 7), ('党组织', 7), ('文艺', 7), ('人人', 7),
             ('年', 6),
             ('初心', 6), ('动力', 6), ('永远', 6), ('面对', 6), ('一系列', 6), ('深化改革', 6), ('完成', 6), ('前列', 6), ('监察', 6),
             ('司法', 6), ('优秀', 6), ('得到', 6), ('中华文化', 6), ('中心', 6), ('力度', 6), ('任务', 6), ('方针', 6), ('交流', 6),
             ('两岸关 系', 6), ('外交', 6), ('良好', 6), ('学习', 6), ('理想信念', 6), ('腐', 6), ('许多', 6), ('存在', 6), ('关心', 6),
             ('共同富裕', 6), ('公平', 6), ('满足', 6), ('一百年', 6), ('先进', 6), ('伟大工程', 6), ('系统', 6), ('鼓励', 6), ('六', 6),
             ('法律', 6), ('能够', 6), ('防治', 6), ('有序', 6), ('消费', 6), ('网络', 6), ('服务体系', 6), ('地区', 6), ('各类', 6),
             ('防止', 6),
             ('贸易', 6), ('行使', 6), ('现实', 6), ('伟大胜利', 5), ('谋', 5), ('幸福', 5)]
    # words = [(u'\uf069', random.randint(20,500)),(u'\uf1fa', random.randint(20,500)),(u'\uf29e', random.randint(20,500)),(u'\uf1b9', random.randint(20,500)),(u'\uf04a', random.randint(20,500)),(u'\uf24e', random.randint(20,500)),(u'\uf05e', random.randint(20,500)),(u'\uf2d5', random.randint(20,500)),(u'\uf19c', random.randint(20,500)),(u'\uf080', random.randint(20,500)),(u'\uf080', random.randint(20,500)),(u'\uf02a', random.randint(20,500)),(u'\uf0c9', random.randint(20,500)),(u'\uf2cd', random.randint(20,500)),(u'\uf2cd', random.randint(20,500)),(u'\uf240', random.randint(20,500)),(u'\uf244', random.randint(20,500)),(u'\uf243', random.randint(20,500)),(u'\uf242', random.randint(20,500)),(u'\uf241', random.randint(20,500)),(u'\uf240', random.randint(20,500)),(u'\uf244', random.randint(20,500)),(u'\uf240', random.randint(20,500)),(u'\uf242', random.randint(20,500)),(u'\uf243', random.randint(20,500)),(u'\uf241', random.randint(20,500)),(u'\uf236', random.randint(20,500)),(u'\uf0fc', random.randint(20,500)),(u'\uf1b4', random.randint(20,500)),(u'\uf1b5', random.randint(20,500)),(u'\uf0f3', random.randint(20,500)),(u'\uf0a2', random.randint(20,500)),(u'\uf1f6', random.randint(20,500)),(u'\uf1f7', random.randint(20,500)),(u'\uf206', random.randint(20,500)),(u'\uf1e5', random.randint(20,500)),(u'\uf1fd', random.randint(20,500)),(u'\uf171', random.randint(20,500)),(u'\uf172', random.randint(20,500)),(u'\uf15a', random.randint(20,500)),(u'\uf27e', random.randint(20,500)),(u'\uf29d', random.randint(20,500)),(u'\uf293', random.randint(20,500)),(u'\uf294', random.randint(20,500)),(u'\uf032', random.randint(20,500)),(u'\uf0e7', random.randint(20,500)),(u'\uf1e2', random.randint(20,500)),(u'\uf02d', random.randint(20,500)),(u'\uf02e', random.randint(20,500)),(u'\uf097', random.randint(20,500)),(u'\uf2a1', random.randint(20,500)),(u'\uf0b1', random.randint(20,500)),(u'\uf15a', random.randint(20,500)),(u'\uf188', random.randint(20,500)),(u'\uf1ad', random.randint(20,500)),(u'\uf0f7', random.randint(20,500)),(u'\uf0a1', random.randint(20,500)),(u'\uf140', random.randint(20,500)),(u'\uf207', random.randint(20,500)),(u'\uf20d', random.randint(20,500)),(u'\uf1ba', random.randint(20,500)),(u'\uf1ec', random.randint(20,500)),(u'\uf073', random.randint(20,500)),(u'\uf274', random.randint(20,500)),(u'\uf272', random.randint(20,500)),(u'\uf133', random.randint(20,500)),(u'\uf271', random.randint(20,500)),(u'\uf273', random.randint(20,500)),(u'\uf030', random.randint(20,500)),(u'\uf083', random.randint(20,500)),(u'\uf1b9', random.randint(20,500)),(u'\uf0d7', random.randint(20,500)),(u'\uf0d9', random.randint(20,500)),(u'\uf0da', random.randint(20,500)),(u'\uf150', random.randint(20,500)),(u'\uf191', random.randint(20,500)),(u'\uf152', random.randint(20,500)),(u'\uf151', random.randint(20,500)),(u'\uf0d8', random.randint(20,500)),(u'\uf218', random.randint(20,500)),(u'\uf217', random.randint(20,500)),(u'\uf20a', random.randint(20,500)),(u'\uf1f3', random.randint(20,500)),(u'\uf24c', random.randint(20,500)),(u'\uf1f2', random.randint(20,500)),(u'\uf24b', random.randint(20,500)),(u'\uf1f1', random.randint(20,500)),(u'\uf1f4', random.randint(20,500)),(u'\uf1f5', random.randint(20,500)),(u'\uf1f0', random.randint(20,500)),(u'\uf0a3', random.randint(20,500)),(u'\uf0c1', random.randint(20,500)),(u'\uf127', random.randint(20,500)),(u'\uf00c', random.randint(20,500)),(u'\uf058', random.randint(20,500)),(u'\uf05d', random.randint(20,500)),(u'\uf14a', random.randint(20,500)),(u'\uf046', random.randint(20,500)),(u'\uf13a', random.randint(20,500)),(u'\uf137', random.randint(20,500)),(u'\uf138', random.randint(20,500)),(u'\uf139', random.randint(20,500)),(u'\uf078', random.randint(20,500)),(u'\uf053', random.randint(20,500)),(u'\uf054', random.randint(20,500)),(u'\uf077', random.randint(20,500)),(u'\uf1ae', random.randint(20,500)),(u'\uf268', random.randint(20,500)),(u'\uf111', random.randint(20,500)),(u'\uf10c', random.randint(20,500)),(u'\uf1ce', random.randint(20,500)),(u'\uf1db', random.randint(20,500)),(u'\uf0ea', random.randint(20,500)),(u'\uf017', random.randint(20,500)),(u'\uf24d', random.randint(20,500)),(u'\uf00d', random.randint(20,500)),(u'\uf0c2', random.randint(20,500)),(u'\uf0ed', random.randint(20,500)),(u'\uf0ee', random.randint(20,500)),(u'\uf157', random.randint(20,500)),(u'\uf121', random.randint(20,500)),(u'\uf126', random.randint(20,500)),(u'\uf1cb', random.randint(20,500)),(u'\uf284', random.randint(20,500)),(u'\uf0f4', random.randint(20,500)),(u'\uf013', random.randint(20,500)),(u'\uf085', random.randint(20,500)),(u'\uf0db', random.randint(20,500)),(u'\uf075', random.randint(20,500)),(u'\uf0e5', random.randint(20,500)),(u'\uf27a', random.randint(20,500)),(u'\uf27b', random.randint(20,500)),(u'\uf086', random.randint(20,500)),(u'\uf0e6', random.randint(20,500)),(u'\uf14e', random.randint(20,500)),(u'\uf066', random.randint(20,500)),(u'\uf20e', random.randint(20,500)),(u'\uf26d', random.randint(20,500)),(u'\uf0c5', random.randint(20,500)),(u'\uf1f9', random.randint(20,500)),(u'\uf25e', random.randint(20,500)),(u'\uf09d', random.randint(20,500)),(u'\uf283', random.randint(20,500)),(u'\uf125', random.randint(20,500)),(u'\uf05b', random.randint(20,500)),(u'\uf13c', random.randint(20,500)),(u'\uf1b2', random.randint(20,500)),(u'\uf1b3', random.randint(20,500)),(u'\uf0c4', random.randint(20,500)),(u'\uf0f5', random.randint(20,500)),(u'\uf0e4', random.randint(20,500)),(u'\uf210', random.randint(20,500)),(u'\uf1c0', random.randint(20,500)),(u'\uf2a4', random.randint(20,500)),(u'\uf2a4', random.randint(20,500)),(u'\uf03b', random.randint(20,500)),(u'\uf1a5', random.randint(20,500)),(u'\uf108', random.randint(20,500)),(u'\uf1bd', random.randint(20,500)),(u'\uf219', random.randint(20,500)),(u'\uf1a6', random.randint(20,500)),(u'\uf155', random.randint(20,500)),(u'\uf192', random.randint(20,500)),(u'\uf019', random.randint(20,500)),(u'\uf17d', random.randint(20,500)),(u'\uf2c2', random.randint(20,500)),(u'\uf2c3', random.randint(20,500)),(u'\uf16b', random.randint(20,500)),(u'\uf1a9', random.randint(20,500)),(u'\uf282', random.randint(20,500)),(u'\uf044', random.randint(20,500)),(u'\uf2da', random.randint(20,500)),(u'\uf052', random.randint(20,500)),(u'\uf141', random.randint(20,500)),(u'\uf142', random.randint(20,500)),(u'\uf1d1', random.randint(20,500)),(u'\uf0e0', random.randint(20,500)),(u'\uf003', random.randint(20,500)),(u'\uf2b6', random.randint(20,500)),(u'\uf2b7', random.randint(20,500)),(u'\uf199', random.randint(20,500)),(u'\uf299', random.randint(20,500)),(u'\uf12d', random.randint(20,500)),(u'\uf2d7', random.randint(20,500)),(u'\uf153', random.randint(20,500)),(u'\uf153', random.randint(20,500)),(u'\uf0ec', random.randint(20,500)),(u'\uf12a', random.randint(20,500)),(u'\uf06a', random.randint(20,500)),(u'\uf071', random.randint(20,500)),(u'\uf065', random.randint(20,500)),(u'\uf23e', random.randint(20,500)),(u'\uf08e', random.randint(20,500)),(u'\uf14c', random.randint(20,500)),(u'\uf06e', random.randint(20,500)),(u'\uf070', random.randint(20,500)),(u'\uf1fb', random.randint(20,500)),(u'\uf2b4', random.randint(20,500)),(u'\uf09a', random.randint(20,500)),(u'\uf09a', random.randint(20,500)),(u'\uf230', random.randint(20,500)),(u'\uf082', random.randint(20,500)),(u'\uf049', random.randint(20,500)),(u'\uf050', random.randint(20,500)),(u'\uf1ac', random.randint(20,500)),(u'\uf09e', random.randint(20,500)),(u'\uf182', random.randint(20,500)),(u'\uf0fb', random.randint(20,500)),(u'\uf15b', random.randint(20,500)),(u'\uf1c6', random.randint(20,500)),(u'\uf1c7', random.randint(20,500)),(u'\uf1c9', random.randint(20,500)),(u'\uf1c3', random.randint(20,500)),(u'\uf1c5', random.randint(20,500)),(u'\uf1c8', random.randint(20,500)),(u'\uf016', random.randint(20,500)),(u'\uf1c1', random.randint(20,500)),(u'\uf1c5', random.randint(20,500)),(u'\uf1c5', random.randint(20,500)),(u'\uf1c4', random.randint(20,500)),(u'\uf1c7', random.randint(20,500)),(u'\uf15c', random.randint(20,500)),(u'\uf0f6', random.randint(20,500)),(u'\uf1c8', random.randint(20,500)),(u'\uf1c2', random.randint(20,500)),(u'\uf1c6', random.randint(20,500)),(u'\uf0c5', random.randint(20,500)),(u'\uf008', random.randint(20,500)),(u'\uf0b0', random.randint(20,500)),(u'\uf06d', random.randint(20,500)),(u'\uf134', random.randint(20,500)),(u'\uf269', random.randint(20,500)),(u'\uf2b0', random.randint(20,500)),(u'\uf024', random.randint(20,500)),(u'\uf11e', random.randint(20,500)),(u'\uf11d', random.randint(20,500)),(u'\uf0e7', random.randint(20,500)),(u'\uf0c3', random.randint(20,500)),(u'\uf16e', random.randint(20,500)),(u'\uf0c7', random.randint(20,500)),(u'\uf07b', random.randint(20,500)),(u'\uf114', random.randint(20,500)),(u'\uf07c', random.randint(20,500)),(u'\uf115', random.randint(20,500)),(u'\uf031', random.randint(20,500)),(u'\uf2b4', random.randint(20,500)),(u'\uf280', random.randint(20,500)),(u'\uf286', random.randint(20,500)),(u'\uf211', random.randint(20,500)),(u'\uf04e', random.randint(20,500)),(u'\uf180', random.randint(20,500)),(u'\uf2c5', random.randint(20,500)),(u'\uf119', random.randint(20,500)),(u'\uf1e3', random.randint(20,500)),(u'\uf11b', random.randint(20,500)),(u'\uf0e3', random.randint(20,500)),(u'\uf154', random.randint(20,500)),(u'\uf1d1', random.randint(20,500)),(u'\uf013', random.randint(20,500)),(u'\uf085', random.randint(20,500)),(u'\uf22d', random.randint(20,500)),(u'\uf265', random.randint(20,500)),(u'\uf260', random.randint(20,500)),(u'\uf261', random.randint(20,500)),(u'\uf06b', random.randint(20,500)),(u'\uf1d3', random.randint(20,500)),(u'\uf1d2', random.randint(20,500)),(u'\uf09b', random.randint(20,500)),(u'\uf113', random.randint(20,500)),(u'\uf092', random.randint(20,500)),(u'\uf296', random.randint(20,500)),(u'\uf184', random.randint(20,500)),(u'\uf000', random.randint(20,500)),(u'\uf2a5', random.randint(20,500)),(u'\uf2a6', random.randint(20,500)),(u'\uf0ac', random.randint(20,500)),(u'\uf1a0', random.randint(20,500)),(u'\uf0d5', random.randint(20,500)),(u'\uf2b3', random.randint(20,500)),(u'\uf2b3', random.randint(20,500)),(u'\uf0d4', random.randint(20,500)),(u'\uf1ee', random.randint(20,500)),(u'\uf19d', random.randint(20,500)),(u'\uf184', random.randint(20,500)),(u'\uf2d6', random.randint(20,500)),(u'\uf0c0', random.randint(20,500)),(u'\uf0fd', random.randint(20,500)),(u'\uf1d4', random.randint(20,500)),(u'\uf255', random.randint(20,500)),(u'\uf258', random.randint(20,500)),(u'\uf0a7', random.randint(20,500)),(u'\uf0a5', random.randint(20,500)),(u'\uf0a4', random.randint(20,500)),(u'\uf0a6', random.randint(20,500)),(u'\uf256', random.randint(20,500)),(u'\uf25b', random.randint(20,500)),(u'\uf25a', random.randint(20,500)),(u'\uf255', random.randint(20,500)),(u'\uf257', random.randint(20,500)),(u'\uf259', random.randint(20,500)),(u'\uf256', random.randint(20,500)),(u'\uf2b5', random.randint(20,500)),(u'\uf2a4', random.randint(20,500)),(u'\uf292', random.randint(20,500)),(u'\uf0a0', random.randint(20,500)),(u'\uf1dc', random.randint(20,500)),(u'\uf025', random.randint(20,500)),(u'\uf004', random.randint(20,500)),(u'\uf08a', random.randint(20,500)),(u'\uf21e', random.randint(20,500)),(u'\uf1da', random.randint(20,500)),(u'\uf015', random.randint(20,500)),(u'\uf0f8', random.randint(20,500)),(u'\uf236', random.randint(20,500)),(u'\uf254', random.randint(20,500)),(u'\uf251', random.randint(20,500)),(u'\uf252', random.randint(20,500)),(u'\uf253', random.randint(20,500)),(u'\uf253', random.randint(20,500)),(u'\uf252', random.randint(20,500)),(u'\uf250', random.randint(20,500)),(u'\uf251', random.randint(20,500)),(u'\uf27c', random.randint(20,500)),(u'\uf13b', random.randint(20,500)),(u'\uf246', random.randint(20,500)),(u'\uf2c1', random.randint(20,500)),(u'\uf2c2', random.randint(20,500)),(u'\uf2c3', random.randint(20,500)),(u'\uf20b', random.randint(20,500)),(u'\uf03e', random.randint(20,500)),(u'\uf2d8', random.randint(20,500)),(u'\uf01c', random.randint(20,500)),(u'\uf03c', random.randint(20,500))]
    words = sorted(words, key=lambda k: -k[1])

    # 字体文件
    font_file = 'C:/Windows/Fonts/SIMHEI.ttf'

    # 画布
    width = 600
    height = 600
    img = Image.new("RGBA", (width, height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # [优化] 策略1: 平面分隔区域
    bounds = Region(width, height, 50)

    # 形状遮罩
    mask_sprite = Sprite()
    mask = Image.open('mask.png').convert('L').resize((width, height))
    mask_sprite.x = 0
    mask_sprite.y = 0
    mask_sprite.img = mask
    mask_sprite.build_tree()
    # bounds.add_sprite(mask_sprite, 0, 0)

    # 颜色映射
    color_mask = Image.open('color_mask.png').resize((width, height))

    # 计算四叉树
    sprites = []
    for (word, size) in words:
        sprite = Sprite()
        sprite.text = word
        sprite.font_size = int(math.sqrt(size) * 4)
        if sprite.font_size < 10:
            sprite.font_size = 10

        font = ImageFont.truetype(font_file, sprite.font_size)
        font = ImageFont.TransposedFont(font)
        size = font.getsize(word)

        # 绘制字符
        img_txt = Image.new('L', (size[0] + 2, size[1] + 2))  # 留边距, 简化运算
        draw_txt = ImageDraw.Draw(img_txt)
        draw_txt.text((1, 1), word, font=font, fill=255)  # 留边距, 简化运算

        # 随机角度旋转
        sprite.rotate = random.randint(-45, 45)
        img_txt = img_txt.rotate(sprite.rotate, resample=Image.NEAREST, expand=1)
        sprite.img = img_txt

        sprite.build_tree()
        sprites.append(sprite)

    # 开始放置词语
    # [优化] 策略2: 略过低概率区域
    prev_sprite = None
    offset = 0

    i = 0
    while i < len(sprites):
        sprite = sprites[i]
        font = ImageFont.truetype(font_file, sprite.font_size)
        font = ImageFont.TransposedFont(font)

        # 判断与上一个词语面积是否差不多
        if not (prev_sprite and (
                (sprite.img.size[0] * sprite.img.size[1]) / (prev_sprite.img.size[0] * prev_sprite.img.size[1]) > 0.8)):
            offset = 0

        # 寻找位置
        x, y, offset = find_position(sprite, bounds, offset)

        # 退出策略, 根据需要调整
        if x == None:
            if not prev_sprite:
                break
            prev_sprite = None
            offset = 0
            continue

        if x > width or x < 0 or y > height or y < 0:
            if not prev_sprite:
                break
            prev_sprite = None
            offset = 0
            continue

        # 找到一个位置
        print('放置第 {} 个词语: {} at {} {}'.format(i, sprite.text, x, y))

        i += 1
        prev_sprite = sprite
        bounds.add_sprite(sprite, x, y)
        sprite.x = x
        sprite.y = y

        # 在画布上绘制单词
        size = font.getsize(sprite.text)
        img_txt = Image.new('RGBA', (size[0] + 2, size[1] + 2))
        draw_txt = ImageDraw.Draw(img_txt)
        color = color_mask.getpixel((x, y))  # 从颜色映射提取颜色

        draw_txt.text((1, 1), sprite.text, font=font, fill=color)

        # 部分系统中, PIL 库绘制的文字边缘有黑边, 手动去除
        r, g, b, a = img_txt.split()
        r = r.point(lambda x: color[0])
        g = g.point(lambda x: color[1])
        b = b.point(lambda x: color[2])
        img_txt = Image.merge('RGBA', (r, g, b, a))

        img_txt = img_txt.rotate(sprite.rotate, resample=Image.BILINEAR, expand=1)
        img.alpha_composite(img_txt, (x, y))

    img.show()
    img.save('wordcloud.png', 'PNG')