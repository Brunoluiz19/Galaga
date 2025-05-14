import pygame
import sys
import os
import subprocess

# Inicializa o pygame
pygame.init()
# Inicia o mixer e carrega a música de início
pygame.mixer.init()
pygame.mixer.music.load("melhor_som_final.mp3")
pygame.mixer.music.play(1)  # 0 = toca uma vez

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ranking")

FONT = pygame.font.SysFont('Orbitron', 28)
LARGE_FONT = pygame.font.SysFont('Orbitron', 40)
COLOR_TEXT = (255, 255, 255)
BG_COLOR = (10, 15, 37)
BUTTON_COLOR = (50, 50, 150)
BUTTON_HIGHLIGHT = (100, 100, 200)

ranking_file = "ranking.txt"

def carregar_ranking():
    if not os.path.exists(ranking_file):
        return []
    with open(ranking_file, "r") as file:
        lines = file.readlines()
        return [line.strip().split(",") for line in lines]

def salvar_ranking(ranking):
    with open(ranking_file, "w") as file:
        for nome, pontos in ranking:
            file.write(f"{nome},{pontos}\n")

def inserir_pontuacao(nova_pontuacao):
    ranking = carregar_ranking()
    ranking = [(nome, int(p)) for nome, p in ranking]
    if len(ranking) < 10 or nova_pontuacao > ranking[-1][1]:
        nome = obter_nome()
        ranking.append((nome, nova_pontuacao))
        ranking.sort(key=lambda x: x[1], reverse=True)
        ranking = ranking[:10]
        salvar_ranking(ranking)

def obter_nome():
    nome = ""
    clock = pygame.time.Clock()
    while True:
        screen.fill(BG_COLOR)
        texto = LARGE_FONT.render("Digite suas iniciais (3 letras):", True, COLOR_TEXT)
        screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2 - 80))
        texto_nome = LARGE_FONT.render(nome, True, COLOR_TEXT)
        screen.blit(texto_nome, (WIDTH // 2 - texto_nome.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(nome) == 3:
                    return nome.upper()
                elif event.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                elif event.unicode.isalpha() and len(nome) < 3:
                    nome += event.unicode.upper()
        clock.tick(30)

def desenhar_botao(texto, rect, ativo):
    cor = BUTTON_HIGHLIGHT if ativo else BUTTON_COLOR
    pygame.draw.rect(screen, cor, rect, border_radius=10)
    texto_surface = FONT.render(texto, True, COLOR_TEXT)
    screen.blit(texto_surface, (
        rect.x + (rect.width - texto_surface.get_width()) // 2,
        rect.y + (rect.height - texto_surface.get_height()) // 2
    ))

def mostrar_ranking():
    ranking = carregar_ranking()
    ranking = [(nome, int(p)) for nome, p in ranking]

    botao_jogar = pygame.Rect(100, 620, 180, 50)
    botao_inicio = pygame.Rect(320, 620, 180, 50)

    clock = pygame.time.Clock()
    esperando = True
    while esperando:
        screen.fill(BG_COLOR)

        titulo = LARGE_FONT.render("TOP 10 RANKING", True, COLOR_TEXT)
        screen.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, 40))

        for i, (nome, pontos) in enumerate(ranking):
            texto = FONT.render(f"{i+1}. {nome} - {pontos}", True, COLOR_TEXT)
            screen.blit(texto, (100, 100 + i * 45))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        desenhar_botao("Jogar Novamente", botao_jogar, botao_jogar.collidepoint(mouse_pos))
        desenhar_botao("Início", botao_inicio, botao_inicio.collidepoint(mouse_pos))

        if mouse_click:
            if botao_jogar.collidepoint(mouse_pos):
                pygame.quit()
                subprocess.run([sys.executable, "tela_rodando.py"])
                sys.exit()
            elif botao_inicio.collidepoint(mouse_pos):
                pygame.quit()
                subprocess.run([sys.executable, "tela_inicial.py"])
                sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            nova_pontuacao = int(sys.argv[1])
            inserir_pontuacao(nova_pontuacao)
        except ValueError:
            print("Erro: valor de pontuação inválido.")
    mostrar_ranking()
    pygame.quit()
    sys.exit()
