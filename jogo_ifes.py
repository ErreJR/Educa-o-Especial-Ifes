import pygame
import sys
import random

# Inicializa o pygame
pygame.init()

# Cores
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
BROWN = (139, 69, 19)
DARK_GREEN = (34, 139, 34)
GRAY = (169, 169, 169)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DARK_BROWN = (101, 67, 33)
GREEN = (34, 177, 76)
BLACK = (0, 0, 0)

# Ativando a tela cheia
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Física Adaptada")

# Fontes
font = pygame.font.SysFont(None, 55)

# Carrega a imagem da instituição
instituicao_image = pygame.image.load('/storage/emulated/0/Python/IFES.jpg')  # Substitua 'instituicao_logo.png' pelo nome do arquivo da sua imagem
instituicao_image = pygame.transform.scale(instituicao_image, (300, 300))
instituicao_rect = instituicao_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))

# Botão "Iniciar" (flutuante)
button_width, button_height = 200, 100
start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 100, button_width, button_height)
button_color = DARK_GREEN
button_hover_color = (50, 205, 50)  # Cor quando o mouse passa por cima

# Botões de controle do jogo
button_size = 50
left_button = pygame.Rect(50, HEIGHT // 2 - button_size // 2, button_size, button_size)
stop_button = pygame.Rect(WIDTH // 2 - button_size // 2, HEIGHT // 2 - button_size // 2, button_size, button_size)
right_button = pygame.Rect(WIDTH - 50 - button_size, HEIGHT // 2 - button_size // 2, button_size, button_size)

left_color = GREEN
stop_color = BLACK
right_color = DARK_GREEN

# Velocidade e aceleração
velocity = 0
acceleration = 0.1
friction = -0.05

# Elementos do cenário
tree_positions = [(random.randint(0, WIDTH), HEIGHT // 2 + 150) for _ in range(10)]
mountain_positions = [(random.randint(0, WIDTH), HEIGHT // 2 - 100) for _ in range(5)]
cloud_positions = [(random.randint(0, WIDTH), random.randint(50, 200)) for _ in range(5)]

# Função para desenhar texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Função para desenhar árvores
def draw_tree(surface, x, y):
    pygame.draw.rect(surface, BROWN, (x, y, 20, 40))
    pygame.draw.polygon(surface, DARK_GREEN, [(x - 30, y), (x + 50, y), (x + 10, y - 60)])

# Função para desenhar montanhas
def draw_mountain(surface, x, y):
    pygame.draw.polygon(surface, GRAY, [(x - 100, y), (x + 100, y), (x, y - 150)])

# Função para desenhar nuvens
def draw_cloud(surface, x, y):
    pygame.draw.ellipse(surface, WHITE, (x, y, 120, 60))

# Função para desenhar o sol
def draw_sun(surface, x, y):
    pygame.draw.circle(surface, YELLOW, (x, y), 50)

# Função para desenhar o rio
def draw_river(surface, x, y, width, height):
    pygame.draw.rect(surface, DARK_BLUE, (x, y, width, height))

# Função para desenhar um dinossauro simples
def draw_dino(surface, x, y):
    # Corpo
    pygame.draw.ellipse(surface, GREEN, (x, y, 100, 50))
    pygame.draw.rect(surface, GREEN, (x + 30, y + 30, 40, 30))
    
    # Cabeça
    pygame.draw.circle(surface, GREEN, (x + 100, y + 25), 25)
    
    # Olho
    pygame.draw.circle(surface, WHITE, (x + 115, y + 15), 5)
    pygame.draw.circle(surface, BLACK, (x + 115, y + 15), 3)
    
    # Pernas
    pygame.draw.rect(surface, GREEN, (x + 10, y + 50, 20, 40))
    pygame.draw.rect(surface, GREEN, (x + 70, y + 50, 20, 40))
    
    # Cauda
    pygame.draw.polygon(surface, GREEN, [(x, y + 25), (x - 50, y + 15), (x, y + 35)])

# Função para desenhar o botão "Iniciar" com efeito flutuante
def draw_button(rect, text, color, hover_color, surface):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect, border_radius=10)
    else:
        pygame.draw.rect(surface, color, rect, border_radius=10)
    
    draw_text(text, font, WHITE, surface, rect.centerx, rect.centery)

# Função para a tela inicial
def main_menu():
    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, (0, HEIGHT * 0.7, WIDTH, HEIGHT * 0.3))

        # Desenha a imagem da instituição
        screen.blit(instituicao_image, instituicao_rect)

        # Desenha o botão "Iniciar"
        draw_button(start_button, 'Iniciar', button_color, button_hover_color, screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    game()

# Função para o jogo
def game():
    global velocity
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Controla os botões de movimento
        if keys[pygame.K_LEFT]:
            velocity += acceleration
        if keys[pygame.K_RIGHT]:
            velocity -= acceleration
        if keys[pygame.K_DOWN]:
            if velocity > 0:
                velocity += friction
            elif velocity < 0:
                velocity -= friction
            if abs(velocity) < 0.1:
                velocity = 0

        # Atualiza a posição dos elementos do cenário
        for i in range(len(tree_positions)):
            tree_positions[i] = (tree_positions[i][0] + velocity, tree_positions[i][1])
            if tree_positions[i][0] < -50:
                tree_positions[i] = (WIDTH + 50, tree_positions[i][1])

        for i in range(len(mountain_positions)):
            mountain_positions[i] = (mountain_positions[i][0] + velocity // 2, mountain_positions[i][1])
            if mountain_positions[i][0] < -100:
                mountain_positions[i] = (WIDTH + 100, mountain_positions[i][1])

        for i in range(len(cloud_positions)):
            cloud_positions[i] = (cloud_positions[i][0] + velocity // 3, cloud_positions[i][1])
            if cloud_positions[i][0] < -120:
                cloud_positions[i] = (WIDTH + 120, cloud_positions[i][1])

        # Desenha o cenário
        screen.fill(LIGHT_BLUE)
        draw_sun(screen, WIDTH - 100, 100)

        # Desenha as montanhas
        for pos in mountain_positions:
            draw_mountain(screen, pos[0], pos[1])

        # Desenha o rio
        draw_river(screen, 0, HEIGHT // 2 + 150, WIDTH, 100)

        # Desenha as árvores
        for pos in tree_positions:
            draw_tree(screen, pos[0], pos[1])

        # Desenha as nuvens
        for pos in cloud_positions:
            draw_cloud(screen, pos[0], pos[1])

        # Desenha o dinossauro
        draw_dino(screen, WIDTH // 2 - 50, HEIGHT // 2 + 100)

        # Desenha os botões
        draw_button(left_button, '←', left_color, left_color, screen)
        draw_button(stop_button, '■', stop_color, stop_color, screen)
        draw_button(right_button, '→', right_color, right_color, screen)

        # Atualiza a tela
        pygame.display.update()

        # Limita a velocidade máxima
        if velocity > 5:
            velocity = 5
        elif velocity < -5:
            velocity = -5

        # Controla a fricção para parar o movimento gradualmente
        if velocity > 0:
            velocity += friction
        elif velocity < 0:
            velocity -= friction
        if abs(velocity) < 0.1:
            velocity = 0

# Chama o menu principal
main_menu()