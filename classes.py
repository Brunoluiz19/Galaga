import pygame
import random
import sys
import math
from cores import (cor_tiro_jogador,cor_tiro_duplo_jogador,)
from tela_rodando import (
largura_tiro,
altura_tiro,
velocidade_tiro_jogador,
velocidade_tiro_inimigo,
tipo_inimigo,
cor_tiro_inimigo,)

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
        self.color = color if color else (cor_tiro_jogador if self.from_player else cor_tiro_inimigo)

    def update(self):
        self.y -= self.speed if self.from_player else -self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def off_screen(self):
        return self.y < -self.height or self.y > altura + self.height
    
# Inimigo 

class inimigo:
    def _init_(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.dead = False
        self.width = 30
        self.height = 24
        self.shoot_cooldown = random.randint(60, 180)
        self.move_direction = 1
        self.base_y = y
        self.phase = random.uniform(0, 2 * math.pi)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.set_attributes_by_kind()
        self.move_speed = 0.7 * self.type['speed_factor']
        self.amplitude = 18

    def set_attributes_by_kind(self):
        mapping = {'vermelho': 'red', 'verde': 'green', 'azul': 'blue', 'ciano': 'cyan'}
        enemy_name = mapping.get(self.kind, 'red')
        self.type = next(e for e in tipo_inimigo if e['name'] == enemy_name)
        self.hp = self.type['hp']
        self.color = self.type['cor']

    def update(self):
        if self.dead: return
        self.phase += 0.03
        self.x += self.move_direction * self.move_speed
        self.y = self.base_y + self.amplitude * math.sin(self.phase)
        if self.x < 5: self.move_direction = 1
        elif self.x + self.width > largura - 5: self.move_direction = -1
        self.rect.topleft = (self.x, self.y)
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = random.randint(60, 180)
            if random.random() < 0.5:
                return self.shoot()
        return None

    def shoot(self):
        bullets = []
        for i in range(self.type['tiros']):
            offset = -10 if i == 0 else 10
            bullet = tiro(self.x + self.width / 2 - largura_tiro / 2 + offset, self.y + self.height, velocidade_tiro_inimigo, from_player=False, damage=self.type['dano'], color=self.type['cor_tiro'])
            bullets.append(bullet)
        return bullets

    def draw(self, surface):
        if self.dead: return
        points = [(self.x + self.width / 2, self.y), (self.x + self.width * 0.8, self.y + self.height), (self.x + self.width * 0.2, self.y + self.height)]
        pygame.draw.polygon(surface, self.type['cor'], points)
        pygame.draw.circle(surface, (0, 0, 0), (int(self.x + self.width / 2), int(self.y + self.height * 0.6)), 6)
        pygame.draw.circle(surface, self.type['cor'], (int(self.x + self.width / 2), int(self.y + self.height * 0.6)), 6, 2)