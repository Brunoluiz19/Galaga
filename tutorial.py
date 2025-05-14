import pygame
import sys
import subprocess

# Inicialização do pygame
pygame.init()
# Inicia o mixer e carrega a música de início
pygame.mixer.init()
pygame.mixer.music.load("som_telai.mp3")
pygame.mixer.music.play(1)  # 0 = toca uma vez

# Constantes
largura, altura = 1000, 800
FONT = pygame.font.SysFont("Arial", 24)
TITLE_FONT = pygame.font.SysFont("Arial", 36, bold=True)

# Tela
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Tutorial")

# Função auxiliar para desenhar texto
def draw_text(surface, text, x, y, font=FONT, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Função do tutorial com fundo branco
def show_tutorial():
    tutorial_running = True
    while tutorial_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                pygame.quit()
                subprocess.run([sys.executable, "tela_inicial.py"])
                sys.exit()

        screen.fill((255, 255, 255))  # Fundo branco

        y = 40
        draw_text(screen, "TUTORIAL", largura // 2 - 80, y, TITLE_FONT)
        y += 60

        draw_text(screen, "COMANDOS:", 60, y)
        y += 30
        draw_text(screen, "Setas ← → ↑ ↓: mover a nave", 80, y)
        y += 30
        draw_text(screen, "Barra de espaço: atirar", 80, y)

        y += 50
        draw_text(screen, "TIPOS DE INIMIGOS:", 60, y)
        y += 30
        draw_text(screen, "Azul: fraco e lento (100 pontos)", 80, y)
        y += 30
        draw_text(screen, "Verde: resistente (tem 2 de vida e tira 1 de dano)(200 pontos)", 80, y)
        y += 30
        draw_text(screen, "Vermelho: rápido e fraco (so tem 1 de vida porem seus tiros tiram 2 vidas)(250 pontos)", 80, y)
        y += 30
        draw_text(screen, "Magenta: muito resistente e perigoso (4 de vida e da um tiro duplo)(500 pontos)", 80, y)

        y += 50
        draw_text(screen, "POWER-UPS:", 60, y)
        y += 30
        draw_text(screen, "🟢 Verde água: Escudo temporário", 80, y)
        y += 30
        draw_text(screen, "🟡 Amarelo: Tiro duplo por tempo limitado", 80, y)
        y += 30
        draw_text(screen, "💖 Rosa: Ganha uma vida extra", 80, y)

        y += 50
        draw_text(screen, "Pressione qualquer tecla para voltar...", largura // 2 - 180, y, FONT, (100, 100, 100))

        pygame.display.flip()

# Execução principal
if __name__ == "__main__":
    show_tutorial()
