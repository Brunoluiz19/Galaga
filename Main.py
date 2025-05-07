import pygame
from cores import branco

pygame.init()

# Medições da tela 
largura = 800
altura = 600

# Inicia a tela 
tela = pygame.display.set_mode((largura,altura))

# Nome do jogo 
pygame.display.set_caption("GALAGA")

# Define o fundo  
cor_fundo = (branco)
