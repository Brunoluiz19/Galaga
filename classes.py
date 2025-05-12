import pygame
import random
import sys
import math
from cores import (cor_tiro_jogador,cor_tiro_duplo_jogador,)
from tela_rodando import (
largura_tiro,
altura_tiro,
velocidade_tiro_jogador,
velocidade_tiro_inimigo)

largura,altura = 1000, 800

# tiro 
class tiro:
    def _init_(self, x, y, speed, from_player=True, damage=1, color=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = largura_tiro
        self.height = altura_tiro
        self.from_player = from_player
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.damage = damage
        self.color = color if color else (cor_tiro_jogador if self.from_player else COLOR_BULLET_ENEMY)

    def update(self):
        self.y -= self.speed if self.from_player else -self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def off_screen(self):
        return self.y < -self.height or self.y > altura + self.height