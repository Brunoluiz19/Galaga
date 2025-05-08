import os
import pygame
import sys
import subprocess
from cores import branco

# Centraliza a janela
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

# Medições da tela 
largura = 1000
altura = 800

# Inicia a tela 
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("GALAGA")

# Carrega e redimensiona o fundo
fundos = pygame.image.load("titulo.png")  
fundo = pygame.transform.scale(fundos, (largura, altura))

# Configuração do botão START
fonte_subtitulo = pygame.font.Font(None, 45)  
texto = fonte_subtitulo.render('START', True, (255, 36, 0))  
titulo_pos = (largura // 2 - texto.get_width() // 2, altura - 150)  
rect_start = pygame.Rect(titulo_pos[0], titulo_pos[1], texto.get_width(), texto.get_height())

jogo = True

while jogo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_start.collidepoint(evento.pos):
                pygame.quit()
                subprocess.run([sys.executable, "tela_rodando.py"])
                sys.exit()

    tela.blit(fundo, (0, 0))
    tela.blit(texto, titulo_pos)
    pygame.display.flip()
