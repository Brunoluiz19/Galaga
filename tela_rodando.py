import pygame
import random
import sys
import math
import subprocess
from classes import (tiro, inimigo, PowerUp, Game)
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

pygame.init()

largura,altura = 1000, 800
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("GALAGA")

# Carregar e redimensionar imagem de fundo
background_image = pygame.image.load("fundo_roxo.jpg")
background_image = pygame.transform.scale(background_image, (largura, altura))

FONT = pygame.font.SysFont('Orbitron', 20, bold=True)
LARGE_FONT = pygame.font.SysFont('Orbitron', 32, bold=True)
clock = pygame.time.Clock()
FPS = 60

# configuração jogador

largura_jogador = 50
altura_jogador = 38
velocidade_jogador = 5

# configuração do tiro
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

#Configuração dos inimigos 

tipo_inimigo = [
    {'name': 'red', 'color': cor_inimigo_vermelho, 'speed_factor': 1.0, 'points': 250, 'hp': 1, 'shots': 1, 'damage': 2, 'zigzag': False, 'bullet_color': cor_tiro_2x_dano},
    {'name': 'green', 'color': cor_inimigo_verde, 'speed_factor': 1.2, 'points': 200, 'hp': 2, 'shots': 1, 'damage': 1, 'zigzag': False, 'bullet_color': cor_tiro_inimigo},
    {'name': 'blue', 'color': cor_inimigo_azul, 'speed_factor': 0.8, 'points': 100, 'hp': 1, 'shots': 1, 'damage': 1, 'zigzag': False, 'bullet_color': cor_tiro_inimigo},
    {'name': 'purple', 'color': cor_inimigo_roxo, 'speed_factor': 1.0, 'points': 500, 'hp': 4, 'shots': 2, 'damage': 1, 'zigzag': False, 'bullet_color': cor_tiro_inimigo},
]

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

if __name__ == "_main_":
    main()