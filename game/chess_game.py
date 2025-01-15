import pygame
import sys

# Inicializar Pygame
pygame.init()

# Constantes
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
HIGHLIGHT = (0, 255, 0)

# Configurar la ventana
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Ajedrez')

class Piece:
    def __init__(self, team, type, image, value):
        self.team = team
        self.type = type
        self.image = image
        self.value = value
        self.has_moved = False

class Chess:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 'white'
        self.selected_piece = None
        self.selected_pos = None
        self.load_images()
        self.setup_board()

    def load_images(self):
        self.images = {}
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        for piece in pieces:
            self.images[f'white_{piece}'] = pygame.transform.scale(
                pygame.image.load(f'chess_pieces/white_{piece}.png'),
                (SQUARE_SIZE, SQUARE_SIZE)
            )
            self.images[f'black_{piece}'] = pygame.transform.scale(
                pygame.image.load(f'chess_pieces/black_{piece}.png'),
                (SQUARE_SIZE, SQUARE_SIZE)
            )

    def setup_board(self):
        # Configurar piezas negras
        self.board[0][0] = Piece('black', 'rook', 'black_rook', 5)
        self.board[0][1] = Piece('black', 'knight', 'black_knight', 3)
        self.board[0][2] = Piece('black', 'bishop', 'black_bishop', 3)
        self.board[0][3] = Piece('black', 'queen', 'black_queen', 9)
        self.board[0][4] = Piece('black', 'king', 'black_king', 100)
        self.board[0][5] = Piece('black', 'bishop', 'black_bishop', 3)
        self.board[0][6] = Piece('black', 'knight', 'black_knight', 3)
        self.board[0][7] = Piece('black', 'rook', 'black_rook', 5)

        # Configurar peones negros
        for i in range(BOARD_SIZE):
            self.board[1][i] = Piece('black', 'pawn', 'black_pawn', 1)

        # Configurar piezas blancas
        self.board[7][0] = Piece('white', 'rook', 'white_rook', 5)
        self.board[7][1] = Piece('white', 'knight', 'white_knight', 3)
        self.board[7][2] = Piece('white', 'bishop', 'white_bishop', 3)
        self.board[7][3] = Piece('white', 'queen', 'white_queen', 9)
        self.board[7][4] = Piece('white', 'king', 'white_king', 100)
        self.board[7][5] = Piece('white', 'bishop', 'white_bishop', 3)
        self.board[7][6] = Piece('white', 'knight', 'white_knight', 3)
        self.board[7][7] = Piece('white', 'rook', 'white_rook', 5)

        # Configurar peones blancos
        for i in range(BOARD_SIZE):
            self.board[6][i] = Piece('white', 'pawn', 'white_pawn', 1)

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(screen, color, 
                               (col * SQUARE_SIZE, row * SQUARE_SIZE, 
                                SQUARE_SIZE, SQUARE_SIZE))

                piece = self.board[row][col]
                if piece:
                    screen.blit(self.images[piece.image],
                              (col * SQUARE_SIZE, row * SQUARE_SIZE))

        if self.selected_pos:
            row, col = self.selected_pos
            pygame.draw.rect(screen, HIGHLIGHT,
                           (col * SQUARE_SIZE, row * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE), 3)

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        valid_moves = []

        if not piece:
            return valid_moves

        if piece.type == 'pawn':
            direction = 1 if piece.team == 'black' else -1
            
            # Movimiento hacia adelante
            if 0 <= row + direction < 8 and not self.board[row + direction][col]:
                valid_moves.append((row + direction, col))
                
                # Movimiento doble inicial
                if ((piece.team == 'black' and row == 1) or 
                    (piece.team == 'white' and row == 6)):
                    if not self.board[row + 2 * direction][col]:
                        valid_moves.append((row + 2 * direction, col))

            # Capturas
            for c in [-1, 1]:
                if (0 <= col + c < 8 and 0 <= row + direction < 8 and
                    self.board[row + direction][col + c] and
                    self.board[row + direction][col + c].team != piece.team):
                    valid_moves.append((row + direction, col + c))

        return valid_moves

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.selected_piece:
            # Mover pieza
            if (row, col) in self.get_valid_moves(*self.selected_pos):
                old_row, old_col = self.selected_pos
                self.board[row][col] = self.selected_piece
                self.board[old_row][old_col] = None
                self.selected_piece = None
                self.selected_pos = None
                self.turn = 'black' if self.turn == 'white' else 'white'
            else:
                self.selected_piece = None
                self.selected_pos = None
        else:
            # Seleccionar pieza
            piece = self.board[row][col]
            if piece and piece.team == self.turn:
                self.selected_piece = piece
                self.selected_pos = (row, col)

def main():
    chess = Chess()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                chess.handle_click(event.pos)

        screen.fill(WHITE)
        chess.draw_board()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()