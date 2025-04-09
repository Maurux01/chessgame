import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
HIGHLIGHT = (0, 255, 0)

# Configure the window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Chess')

class Piece:
    def __init__(self, team, piece_type, image, value):
        self.team = team
        self.type = piece_type
        self.image = image
        self.value = value
        self.has_moved = False

    def __repr__(self):
         return f"{self.team.capitalize()} {self.type.capitalize()}"

class Chess:
    def __init__(self):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.turn = 'white'
        self.selected_piece = None
        self.selected_pos = None
        self.load_images()
        self.setup_board()
        self.valid_moves = []

    def load_images(self):
        self.images = {}
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        for piece in pieces:
            try:
                self.images[f'white_{piece}'] = pygame.transform.scale(
                    pygame.image.load(f'chess_pieces/white_{piece}.png'),
                    (SQUARE_SIZE, SQUARE_SIZE)
                )
                self.images[f'black_{piece}'] = pygame.transform.scale(
                    pygame.image.load(f'chess_pieces/black_{piece}.png'),
                    (SQUARE_SIZE, SQUARE_SIZE)
                )
            except FileNotFoundError:
                print(f"Error: Image file for {piece} not found. Check the 'chess_pieces' directory.")
                sys.exit()

    def setup_board(self):
        # Define the initial board setup
        initial_board = [
            ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook'],
            ['pawn'] * BOARD_SIZE,
            [None] * BOARD_SIZE,
            [None] * BOARD_SIZE,
            [None] * BOARD_SIZE,
            [None] * BOARD_SIZE,
            ['pawn'] * BOARD_SIZE,
            ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        ]

        # Place pieces on the board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece_type = initial_board[row][col]
                if piece_type:
                    team = 'black' if row < 2 else 'white'
                    image_name = f'{team}_{piece_type}'
                    self.board[row][col] = Piece(team, piece_type, image_name, self.get_piece_value(piece_type))

    def get_piece_value(self, piece_type):
        piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 100}
        return piece_values.get(piece_type, 0)

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

        # Highlight valid moves
        if self.selected_pos:
            for move in self.valid_moves:
                pygame.draw.rect(screen, HIGHLIGHT,
                               (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE), 3)

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        valid_moves = []

        if not piece:
            return valid_moves

        if piece.type == 'pawn':
            direction = 1 if piece.team == 'black' else -1

            # Move forward
            new_row = row + direction
            if 0 <= new_row < BOARD_SIZE and not self.board[new_row][col]:
                valid_moves.append((new_row, col))

                # Double move at start
                if ((piece.team == 'black' and row == 1) or
                    (piece.team == 'white' and row == 6)):
                    if not self.board[row + 2 * direction][col] and not self.board[new_row][col]:
                        valid_moves.append((row + 2 * direction, col))

            # Capture diagonally
            for c in [-1, 1]:
                new_col = col + c
                if 0 <= new_col < BOARD_SIZE and 0 <= new_row < BOARD_SIZE and self.board[new_row][new_col]:
                    if self.board[new_row][new_col].team != piece.team:
                        valid_moves.append((new_row, new_col))
        elif piece.type == 'rook':
            valid_moves = self.get_rook_moves(row, col)
        elif piece.type == 'knight':
            valid_moves = self.get_knight_moves(row, col)
        elif piece.type == 'bishop':
            valid_moves = self.get_bishop_moves(row, col)
        elif piece.type == 'queen':
            valid_moves = self.get_queen_moves(row, col)
        elif piece.type == 'king':
            valid_moves = self.get_king_moves(row, col)

        return valid_moves

    def get_rook_moves(self, row, col):
        moves = []
        # Directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            for i in range(1, BOARD_SIZE):
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if not self.board[new_row][new_col]:
                        moves.append((new_row, new_col))
                    else:
                        if self.board[new_row][new_col].team != self.board[row][col].team:
                            moves.append((new_row, new_col))
                        break  # Stop if the path is blocked
                else:
                    break  # Stop if out of bounds
        return moves

    def get_knight_moves(self, row, col):
        moves = []
        # Possible knight moves
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if not self.board[new_row][new_col] or self.board[new_row][new_col].team != self.board[row][col].team:
                    moves.append((new_row, new_col))
        return moves

    def get_bishop_moves(self, row, col):
        moves = []
        # Directions: up-left, up-right, down-left, down-right
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            for i in range(1, BOARD_SIZE):
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                    if not self.board[new_row][new_col]:
                        moves.append((new_row, new_col))
                    else:
                        if self.board[new_row][new_col].team != self.board[row][col].team:
                            moves.append((new_row, new_col))
                        break  # Stop if the path is blocked
                else:
                    break  # Stop if out of bounds
        return moves

    def get_queen_moves(self, row, col):
        # Queen can move like a rook and a bishop
        return self.get_rook_moves(row, col) + self.get_bishop_moves(row, col)

    def get_king_moves(self, row, col):
        moves = []
        # Possible king moves
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
        for dr, dc in king_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < BOARD_SIZE and 0 <= new_col < BOARD_SIZE:
                if not self.board[new_row][new_col] or self.board[new_row][new_col].team != self.board[row][col].team:
                    moves.append((new_row, new_col))
        return moves

    def handle_click(self, pos):
        col = pos[0] // SQUARE_SIZE
        row = pos[1] // SQUARE_SIZE

        if self.selected_piece:
            # Try to move the piece
            if (row, col) in self.valid_moves:
                self.move_piece(self.selected_pos, (row, col))
            # If the click is on the same piece, deselect it
            elif (row, col) == self.selected_pos:
                self.deselect_piece()
            # If the click is on a piece of the same team, select it
            elif self.board[row][col] and self.board[row][col].team == self.turn:
                self.select_piece(row, col)
            # Otherwise, deselect the piece
            else:
                self.deselect_piece()
        else:
            # Select a piece
            self.select_piece(row, col)

    def select_piece(self, row, col):
        piece = self.board[row][col]
        if piece and piece.team == self.turn:
            self.selected_piece = piece
            self.selected_pos = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)

    def deselect_piece(self):
        self.selected_piece = None
        self.selected_pos = None
        self.valid_moves = []

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        self.board[end_row][end_col] = self.selected_piece
        self.board[start_row][start_col] = None
        self.selected_piece.has_moved = True
        self.deselect_piece()
        self.switch_turn()

    def switch_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

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