import pygame

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Crear la ventana
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Ajedrez")

# Cargar imágenes de las piezas
def load_pieces():
    pieces = {}
    names = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for name in names:
            image = pygame.image.load(f"assets/{color}_{name}.png")
            pieces[f"{color}_{name}"] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return pieces

# Dibujar el tablero
def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 1:  # Alternar colores
                pygame.draw.rect(win, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Dibujar piezas
def draw_pieces(win, pieces):
    # Posiciones iniciales para las piezas (ejemplo simplificado)
    start_positions = {
        "white_pawn": [(i, 6) for i in range(8)],
        "black_pawn": [(i, 1) for i in range(8)],
        "white_rook": [(0, 7), (7, 7)],
        "black_rook": [(0, 0), (7, 0)],
        "white_knight": [(1, 7), (6, 7)],
        "black_knight": [(1, 0), (6, 0)],
        "white_bishop": [(2, 7), (5, 7)],
        "black_bishop": [(2, 0), (5, 0)],
        "white_queen": [(3, 7)],
        "black_queen": [(3, 0)],
        "white_king": [(4, 7)],
        "black_king": [(4, 0)],
    }

    for piece, positions in start_positions.items():
        for pos in positions:
            x, y = pos
            win.blit(pieces[piece], (x * SQUARE_SIZE, y * SQUARE_SIZE))

# Bucle principal
def main():
    pieces = load_pieces()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board(win)
        draw_pieces(win, pieces)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
