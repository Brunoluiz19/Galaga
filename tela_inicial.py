import os
import pygame
import sys
import subprocess
from cores import branco,azul

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

# Fonte e cor dos botões
fonte_subtitulo = pygame.font.Font(None, 45)  
cor_botao = azul
cor_hover = branco

# Função para desenhar botão com hover
def desenhar_botao(texto, posicao, rect, mouse_pos):
    if rect.collidepoint(mouse_pos):
        # Desenha uma borda branca ao redor
        pygame.draw.rect(tela, branco, rect.inflate(10, 10), border_radius=5)
    tela.blit(texto, posicao)

# Texto dos botões
texto_start = fonte_subtitulo.render('START', True, cor_botao)  
pos_start = (largura // 2 - texto_start.get_width() // 2, altura - 150)  
rect_start = pygame.Rect(pos_start[0], pos_start[1], texto_start.get_width(), texto_start.get_height())

texto_comandos = fonte_subtitulo.render('COMANDOS', True, cor_botao)
pos_comandos = (largura // 2 - texto_comandos.get_width() // 2, pos_start[1] + 60)
rect_comandos = pygame.Rect(pos_comandos[0], pos_comandos[1], texto_comandos.get_width(), texto_comandos.get_height())

jogo = True

while jogo:
    mouse_pos = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if rect_start.collidepoint(evento.pos):
                pygame.quit()
                subprocess.run([sys.executable, "tela_rodando.py"])
                sys.exit()
            elif rect_comandos.collidepoint(evento.pos):
                pygame.quit()
                subprocess.run([sys.executable, "comandos.py"])
                sys.exit()

    tela.blit(fundo, (0, 0))
    desenhar_botao(texto_start, pos_start, rect_start, mouse_pos)
    desenhar_botao(texto_comandos, pos_comandos, rect_comandos, mouse_pos)
    pygame.display.flip()
