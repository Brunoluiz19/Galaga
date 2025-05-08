import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GALAGA")

# Carregar e redimensionar imagem de fundo
background_image = pygame.image.load("fundo_roxo.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))