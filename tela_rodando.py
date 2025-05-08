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

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GALAGA")

# Carregar e redimensionar imagem de fundo
background_image = pygame.image.load("fundo_roxo.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))