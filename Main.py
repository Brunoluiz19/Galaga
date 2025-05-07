import pygame
import sys
from cores import branco

pygame.init()

# Medições da tela 
largura = 1000
altura = 800

# Inicia a tela 
tela = pygame.display.set_mode((largura, altura))

# Nome do jogo 
pygame.display.set_caption("GALAGA")

# Define o fundo  
fundos = pygame.image.load("titulo.png")  
fundo = pygame.transform.scale(fundos, (largura, altura))

# Configuração do botão START
fonte_subtitulo = pygame.font.Font(None, 45)  # Tamanho e fonte da letra  
texto = fonte_subtitulo.render('START', True, (255,36,0))  # Mensagem e definição da cor 

# Ajusta a posição do botão para que fique abaixo da nave
titulo_pos = (largura // 2 - texto.get_width() // 2, altura - 150)  

jogo = True

while jogo:

    # Verificação de eventos 
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo = False

    # Desenha o fundo na tela
    tela.blit(fundo, (0, 0))

    # Desenha o botão START na tela abaixo da nave
    tela.blit(texto, titulo_pos)

    # Atualiza a tela 
    pygame.display.flip()

# Encerra o Pygame 
pygame.quit()
sys.exit()
