import pygame
import sys
import subprocess

# Inicialização do pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("som_telai.mp3")
pygame.mixer.music.play(1)

# Constantes
largura, altura = 1000, 800
FONT = pygame.font.SysFont("Arial", 24)
TITLE_FONT = pygame.font.SysFont("Arial", 40, bold=True)

# Tela
screen = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Tutorial")

# Carregar imagem de fundo
try:
    fundo = pygame.image.load("galaxia1.jpg")
    fundo = pygame.transform.scale(fundo, (largura, altura))
except:
    fundo = None

# Carregar imagens dos inimigos
try:
    inimigos_imgs = [
        pygame.image.load("inimigo_azul.png").convert_alpha(),   # Azul (fraco e lento)
        pygame.image.load("inimigo_verde.png").convert_alpha(),  # Verde (resistente)
        pygame.image.load("inimigo_vermelho.png").convert_alpha(),  # Vermelho (forte e rápido)
        pygame.image.load("inimigo_roxo.png").convert_alpha()   # Magenta (muito resistente)
    ]
    inimigos_imgs = [pygame.transform.scale(img, (50, 50)) for img in inimigos_imgs]
except:
    inimigos_imgs = [None] * 4  # Se imagens não forem carregadas, evita erro

def draw_text(surface, text, x, y, font=FONT, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_powerup_circle(surface, color, x, y, radius=10):
    pygame.draw.circle(surface, color, (x, y), radius)

# Função do tutorial
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

        # Fundo
        if fundo:
            screen.blit(fundo, (0, 0))
        else:
            screen.fill((255, 255, 255))

        # Caixa semi-transparente
        overlay = pygame.Surface((860, 680))
        overlay.set_alpha(210)
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (70, 60))

        y = 80
        draw_text(screen, "TUTORIAL", largura // 2 - 90, y, TITLE_FONT, (0, 0, 80))
        y += 60

        draw_text(screen, "COMANDOS:", 100, y)
        y += 30
        draw_text(screen, "Setas ← → ↑ ↓ ou ADWS: mover a nave", 120, y)
        y += 30
        draw_text(screen, "Barra de espaço: atirar", 120, y)

        y += 50
        draw_text(screen, "TIPOS DE INIMIGOS:", 100, y)
        y += 30

        inimigos_descricoes = [
            "Azul: fraco e lento (100 pontos)",
            "Verde: resistente (2 de vida, 1 de dano) (200 pontos)",
            "Vermelho: rápido e forte (1 de vida, 2 de dano) (250 pontos)",
            "Magenta: muito resistente (4 de vida, tiro duplo) (500 pontos)"
        ]

        for i in range(4):
            if inimigos_imgs[i]:
                screen.blit(inimigos_imgs[i], (120, y))
            draw_text(screen, inimigos_descricoes[i], 180, y + 10)
            y += 60

        draw_text(screen, "POWER-UPS:", 100, y)
        y += 30
        draw_powerup_circle(screen, (51, 255, 204), 120, y + 10)
        draw_text(screen, "Azul: Escudo temporário", 150, y)
        y += 30
        draw_powerup_circle(screen, (255, 255, 0), 120, y + 10)
        draw_text(screen, "Amarelo: Tiro duplo por tempo limitado", 150, y)
        y += 30
        draw_powerup_circle(screen, (255, 105, 180), 120, y + 10)
        draw_text(screen, "Rosa: Ganha uma vida extra", 150, y)
        y += 30
        draw_powerup_circle(screen, (0, 0, 139), 120, y + 10)
        draw_text(screen, "Azul escuro: tiro atravessa os inimigos", 150, y)

        y += 60
        draw_text(screen, "Pressione qualquer tecla para voltar...", largura // 2 - 190, y, FONT, (80, 80, 80))

        pygame.display.flip()

# Executar o tutorial
show_tutorial()

# Execução principal
if __name__ == "__main__":
    show_tutorial()
