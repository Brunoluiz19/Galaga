import pygame
import random
import sys
import math
from cores import (
cor_jogador,
cor_inimigo_vermelho,
cor_inimigo_verde,
cor_inimigo_azul,
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

linha_inimigo = 4
coluna_inimigo = 7
inimigo_h_espaco = 50
inimigo_v_espaco = 44
inicio_inimigo_x = 25
inicio_inimigo_y = 60
