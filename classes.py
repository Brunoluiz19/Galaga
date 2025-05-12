import pygame
import random
import sys
import math
from cores import (
cor_jogador,
cor_inimigo_vermelho,
cor_inimigo_verde,
cor_inimigo_azul,
cor_inimigo_roxo,
cor_tiro_jogador,
cor_tiro_2x_dano,
cor_tiro_inimigo,
cor_textos,
cor_escudo,
cor_vida,
cor_powerup_escudo,
cor_tiro_duplo_jogador,
                   )
from tela_rodando import (
largura_tiro,
altura_tiro,
velocidade_tiro_jogador,
velocidade_tiro_inimigo,
tipo_inimigo,
cor_tiro_inimigo,
largura_jogador,
altura_jogador,
velocidade_jogador,
qnt_linha_inimigo,
qnt_coluna_inimigo,
inimigo_h_espaco,
inimigo_v_espaco,
inicio_inimigo_x,
inicio_inimigo_y)

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

# power up

class PowerUp:
    def _init_(self, x, y, kind):
        self.x = x
        self.y = y
        self.kind = kind
        self.size = 16
        self.speed = 2
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        color = cor_vida if self.kind == 'vida' else cor_powerup_escudo if self.kind == 'escudo' else cor_tiro_duplo_jogador
        pygame.draw.circle(surface, color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def off_screen(self):
        return self.y > altura

# jogo
class Game:
    def _init_(self):
        self.player_x = largura // 2 - largura_jogador // 2
        self.player_y = altura - 60
        self.player_lives = 5
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.powerups = []
        self.score = 0
        self.running = True
        self.shoot_cooldown = 0
        self.shield_active = False
        self.double_shot = False
        self.shield_timer = 0
        self.double_timer = 0
        self.spawn_enemies()

    def spawn_enemies(self):
        self.enemies.clear()
        kinds = ['azul', 'vermelho', 'verde', 'ciano']
        for row in range(qnt_linha_inimigo):
            for col in range(qnt_coluna_inimigo):
                x = inicio_inimigo_x + col * inimigo_h_espaco
                y = inicio_inimigo_y + row * inimigo_v_espaco
                kind = random.choice(kinds)
                self.enemies.append(inimigo(x, y, kind))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: self.player_x -= velocidade_jogador
        if keys[pygame.K_RIGHT]: self.player_x += velocidade_jogador
        if keys[pygame.K_UP]: self.player_y -= velocidade_jogador
        if keys[pygame.K_DOWN]: self.player_y += velocidade_jogador
        self.player_x = max(0, min(largura - largura_jogador, self.player_x))
        self.player_y = max(altura // 2, min(altura - altura_jogador, self.player_y))

        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.fire_bullet()

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.off_screen():
                self.bullets.remove(bullet)
                continue
            for enemy in self.enemies:
                if not enemy.dead and bullet.rect.colliderect(enemy.rect):
                    enemy.hp -= bullet.damage
                    if enemy.hp <= 0:
                        enemy.dead = True
                        self.score += enemy.type['pontos']
                        if random.random() < 0.15:
                            kind = random.choice(['vida', 'escudo', 'double'])
                            self.powerups.append(PowerUp(enemy.x + 10, enemy.y + 10, kind))
                    self.bullets.remove(bullet)
                break

