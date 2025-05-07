import pygame
import sys
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

jogo = True

while jogo:

    # Verificação de eventos 
    for evento in pygame.event.get():
        if evento.type == pygame.quit:
            jogo = False

    # Preenche a tela de fundo com a cor que foi definida 
    tela.fill(cor_fundo)

    # Atualiza a tela 
    pygame.display.flip()


# Encerra o Pygame 
pygame.quit()
sys.exit()
