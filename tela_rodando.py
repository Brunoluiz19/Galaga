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
import pygame
import random
import sys
import math
import subprocess

pygame.init()

largura, altura = 1000, 800
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("GALAGA")

background_image = pygame.image.load("fundo_roxo.jpg")
background_image = pygame.transform.scale(background_image, (largura, altura))

FONT = pygame.font.SysFont('Orbitron', 20, bold=True)
LARGE_FONT = pygame.font.SysFont('Orbitron', 32, bold=True)
clock = pygame.time.Clock()
FPS = 60
largura_jogador = 50
altura_jogador = 38
velocidade_jogador = 5

largura_tiro = 7
altura_tiro = 13
velocidade_tiro_jogador = 7
velocidade_tiro_inimigo = 3

qnt_linha_inimigo = 6
qnt_coluna_inimigo = 15
inimigo_h_espaco = 50
inimigo_v_espaco = 44
inicio_inimigo_x = 25
inicio_inimigo_y = 60

tipo_inimigo = [
    {'name': 'red', 'cor': cor_inimigo_vermelho, 'speed_factor': 1.0, 'pontos': 250, 'hp': 1, 'tiros': 1, 'dano': 2, 'cor_tiro': cor_tiro_2x_dano},
    {'name': 'green', 'cor': cor_inimigo_verde, 'speed_factor': 1.2, 'pontos': 200, 'hp': 2, 'tiros': 1, 'dano': 1, 'cor_tiro': cor_tiro_inimigo},
    {'name': 'blue', 'cor': cor_inimigo_azul, 'speed_factor': 0.8, 'pontos': 100, 'hp': 1, 'tiros': 1, 'dano': 1, 'cor_tiro': cor_tiro_inimigo},
    {'name': 'purple', 'cor': cor_inimigo_roxo, 'speed_factor': 1.0, 'pontos': 500, 'hp': 4, 'tiros': 2, 'dano': 1, 'cor_tiro': cor_tiro_inimigo},
]

class tiro:
    def __init__(self, x, y, speed, from_player=True, damage=1, color=None):
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

class inimigo:
    def __init__(self, x, y, kind):
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
        mapping = {'vermelho': 'red', 'verde': 'green', 'azul': 'blue', 'ciano': 'purple'}
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

class PowerUp:
    def __init__(self, x, y, kind):
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

class Game:
    def __init__(self):
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
        self.nivel = 0
        self.spawn_enemies()

    def spawn_enemies(self):
        self.enemies.clear()
        self.nivel += 1
        kinds = ['azul', 'vermelho', 'verde', 'ciano']
        for row in range(qnt_linha_inimigo):
            for col in range(qnt_coluna_inimigo):
                x = inicio_inimigo_x + col * inimigo_h_espaco
                y = inicio_inimigo_y + row * inimigo_v_espaco
                kind = random.choice(kinds)
                novo_inimigo = inimigo(x, y, kind)
                novo_inimigo.hp += self.nivel // 3
                novo_inimigo.move_speed *= 1 + (self.nivel * 0.05)
                novo_inimigo.shoot_cooldown = max(30, novo_inimigo.shoot_cooldown - self.nivel * 2)
                self.enemies.append(novo_inimigo)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= velocidade_jogador
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += velocidade_jogador
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_y -= velocidade_jogador
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_y += velocidade_jogador
        self.player_x = max(0, min(largura - largura_jogador, self.player_x))
        self.player_y = max(altura // 2, min(altura - altura_jogador, self.player_y))

        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.fire_bullet()

        for b in self.bullets[:]:
            b.update()
            if b.off_screen():
                self.bullets.remove(b)
                continue
            for inim in self.enemies:
                if not inim.dead and b.rect.colliderect(inim.rect):
                    inim.hp -= b.damage
                    if inim.hp <= 0:
                        inim.dead = True
                        self.score += inim.type['pontos']
                        if random.random() < 0.15:
                            kind = random.choice(['vida', 'escudo', 'double'])
                            self.powerups.append(PowerUp(inim.x + 10, inim.y + 10, kind))
                    self.bullets.remove(b)
                    break

        for inim in self.enemies:
            result = inim.update()
            if result:
                self.enemy_bullets.extend(result)

        for b in self.enemy_bullets[:]:
            b.update()
            if b.off_screen():
                self.enemy_bullets.remove(b)
                continue
            player_rect = pygame.Rect(self.player_x, self.player_y, largura_jogador, altura_jogador)
            if b.rect.colliderect(player_rect):
                if not self.shield_active:
                    self.player_lives -= b.damage
                self.enemy_bullets.remove(b)
                if self.player_lives <= 0:
                    self.running = False

        for p in self.powerups[:]:
            p.update()
            if p.off_screen():
                self.powerups.remove(p)
            else:
                player_rect = pygame.Rect(self.player_x, self.player_y, largura_jogador, altura_jogador)
                if p.rect.colliderect(player_rect):
                    if p.kind == 'vida':
                        self.player_lives += 1
                    elif p.kind == 'escudo':
                        self.shield_active = True
                        self.shield_timer = FPS * 5
                    elif p.kind == 'double':
                        self.double_shot = True
                        self.double_timer = FPS * 5
                    self.powerups.remove(p)

        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False

        if self.double_shot:
            self.double_timer -= 1
            if self.double_timer <= 0:
                self.double_shot = False

        # Verifica se todos os inimigos foram derrotados
        if all(e.dead for e in self.enemies):
            self.spawn_enemies()

    def fire_bullet(self):
        self.shoot_cooldown = 20
        if self.double_shot:
            self.bullets.append(tiro(self.player_x + 6, self.player_y, velocidade_tiro_jogador))
            self.bullets.append(tiro(self.player_x + largura_jogador - 10, self.player_y, velocidade_tiro_jogador))
        else:
            self.bullets.append(tiro(self.player_x + largura_jogador // 2 - largura_tiro // 2, self.player_y, velocidade_tiro_jogador))

    def draw(self, surface):
        surface.blit(background_image, (0, 0))
        draw_player(surface, self.player_x, self.player_y, self.shield_active)
        for b in self.bullets: b.draw(surface)
        for b in self.enemy_bullets: b.draw(surface)
        for inim in self.enemies: inim.draw(surface)
        for p in self.powerups: p.draw(surface)
        draw_text(surface, f"PONTUAÇÃO: {self.score}", 10, 10)
        draw_text(surface, f"VIDAS: {self.player_lives}", largura - 150, 10)
        draw_text(surface, f"NÍVEL: {self.nivel}", largura // 2 - 60, 10)
        pygame.display.flip()

def draw_player(surface, x, y, shield):
    points = [(x + largura_jogador / 2, y), (x + largura_jogador, y + altura_jogador), (x, y + altura_jogador)]
    pygame.draw.polygon(surface, cor_jogador, points)
    pygame.draw.polygon(surface, (0, 214, 255), points, 3)
    pygame.draw.circle(surface, (0, 76, 102), (int(x + largura_jogador / 2), int(y + altura_jogador * 0.6)), 6)
    pygame.draw.circle(surface, cor_jogador, (int(x + largura_jogador / 2), int(y + altura_jogador * 0.6)), 6, 2)
    if shield:
        pygame.draw.circle(surface, cor_escudo, (int(x + largura_jogador / 2), int(y + altura_jogador / 2)), 25, 2)

def draw_text(surface, text, x, y, font=LARGE_FONT):
    surface.blit(font.render(text, True, cor_textos), (x, y))

def main():
    game = Game()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        game.update()
        game.draw(screen)
        clock.tick(FPS)

    pygame.quit()
    subprocess.run([sys.executable, "ranking.py", str(game.score)])
    sys.exit()

if __name__ == "__main__":
    main()
