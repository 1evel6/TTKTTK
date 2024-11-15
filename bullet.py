
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船发射的子弹"""

    def __init__(self, screen, ship):
        """在飞船当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen

        # 在(0, 0)处创建一个表示子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, 3, 15)  # 子弹大小
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 存储用小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = (60, 60, 60)
        self.speed_factor = 1.5

    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.speed_factor
        # 更新子弹的rect位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)