import pygame
import sys
from cores import branco

pygame.init()

# Medições da tela 
largura = 800
altura = 600

# Inicia a tela 
tela = pygame.display.set_mode((largura, altura))

# Nome do jogo 
pygame.display.set_caption("GALAGA")

# Define o fundo  
fundos = pygame.image.load("titulo.png")  
fundo = pygame.transform.scale(fundos, (largura, altura))

jogo = True

while jogo:

    # Verificação de eventos 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Corrigido pygame.quit para pygame.QUIT
            jogo = False

    # Desenha o fundo na tela
    tela.blit(fundo, (0, 0))

    # Atualiza a tela 
    pygame.display.flip()

# Encerra o Pygame 
pygame.quit()
sys.exit()
