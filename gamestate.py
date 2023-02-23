from copy import deepcopy

from pieces.peca import Peca
from pieces.gato import Gato
from pieces.rato import Rato

class Board:

    whites = []
    blacks = []

    # game_mode == 0 : whites down/blacks up
    def __init__(self, game_mode, ai=False, depth=2, log=False):
        self.board = []
        self.game_mode = game_mode
        self.depth = depth
        self.ai = ai
        self.log = log

    def initialize_board(self):
        for i in range(8):
            self.board.append(['vazio' for _ in range(8)])

    def place_pieces(self):
        self.board.clear()
        self.whites.clear()
        self.blacks.clear()
        self.initialize_board()
        self[1][3] = Gato("white",1,3,"\u265C")
        self[6][0] = Rato("black",6,0,"\u265F")
        self[6][1] = Rato("black",6,1,"\u265F")
        self[6][2] = Rato("black",6,2,"\u265F")
        self[6][5] = Rato("black",6,5,"\u265F")
        self[6][6] = Rato("black",6,6,"\u265F")
        self[6][7] = Rato("black",6,7,"\u265F")
        self.save_pieces()

        if self.game_mode != 0:
            self.reverse()

    def save_pieces(self):
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], Peca):
                    if self[i][j].color == 'white':
                        self.whites.append(self[i][j])
                    else:
                        self.blacks.append(self[i][j])

    # history is logged when ai searches for moves
    def make_move(self, piece, x, y, keep_history=False):
        old_x = piece.x
        old_y = piece.y
        if keep_history:
            self.board[old_x][old_y].set_last_eaten(self.board[x][y])
        else:
            if isinstance(self.board[x][y], Peca):
                if self.board[x][y].color == 'white':
                    self.whites.remove(self.board[x][y])
                else:
                    self.blacks.remove(self.board[x][y])
        self.board[x][y] = self.board[old_x][old_y]
        self.board[old_x][old_y] = 'vazio'
        self.board[x][y].set_position(x, y, keep_history)

        return (old_x, old_y)

    def unmake_move(self, piece):
        x = piece.x
        y = piece.y
        self.board[x][y].set_old_position()
        old_x = piece.x
        old_y = piece.y
        self.board[old_x][old_y] = self.board[x][y]
        self.board[x][y] = piece.get_last_eaten()

    def reverse(self):
        self.board = self.board[::-1]
        for i in range(8):
            for j in range(8):
                if isinstance(self.board[i][j], Peca):
                    piece = self.board[i][j]
                    piece.x = i
                    piece.y = j

    def __getitem__(self, item):
        return self.board[item]

    def has_opponent(self, piece, x, y):
        if not self.is_valid_move(x, y):
            return False
        if isinstance(self.board[x][y], Peca):
            return piece.color != self[x][y].color
        return False

    def has_friend(self, piece, x, y):
        if not self.is_valid_move(x, y):
            return False
        if isinstance(self[x][y], Peca):
            return piece.color == self[x][y].color
        return False

    @staticmethod
    def is_valid_move(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def has_empty_block(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        return not isinstance(self[x][y], Peca)

    def get_player_color(self):
        if self.game_mode == 0:
            return 'white'
        return 'black'


    def is_terminal(self):
        terminal1 = self.white_won()
        terminal2 = self.black_won()
        return terminal1 or terminal2

    def white_won(self):
        # Percorre todas as posições do tabuleiro
        for i in range(8):
            for j in range(8):
                # Verifica se há uma peça na posição i, j
                if isinstance(self[i][j], Peca):
                    # Verifica se a peça é um rato preto
                    if isinstance(self[i][j], Rato) and self[i][j].color == 'black':
                        # Se houver um rato preto, o jogo não acabou
                        return False
        # Se não houver ratos pretos no tabuleiro, o jogo acabou e o jogador branco venceu
        return True

    def black_won(self):
        # Se o gato tiver sido eliminado ou algum dos rato tiver chegado ao outro lado do tabuleiro
        if self.has_gato(self.board) == False:
            return True
        else:
            # Se na ultima linha tiver um rato preto, o jogo acabou e o jogador preto venceu
            for i in range(8):
                if isinstance(self[0][i], Rato) and self[0][i].color == 'black':
                    return True
            return False

    def has_moves(self, color):
        total_moves = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], Peca) and self[i][j].color == color:
                    piece = self[i][j]
                    total_moves += len(piece.filter_moves(piece.get_moves(self), self))
                    if total_moves > 0:
                        return True
        return False

    def has_gato(self,matriz):
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if isinstance(matriz[i][j], Gato):
                    return True
        return False

    def evaluate(self):
        white_points = 0
        black_points = 0
        for i in range(8):
            for j in range(8):
                if isinstance(self[i][j], Peca):
                    piece = self[i][j]
                    if piece.color == 'white':
                        white_points += piece.get_score()
                    else:
                        black_points += piece.get_score()
        if self.game_mode == 0:
            return black_points - white_points
        return white_points - black_points

    def __str__(self):
        return str(self[::-1]).replace('], ', ']\n')

    def __repr__(self):
        return 'Board'

    # Apenas no log
    def unicode_array_repr(self):
        data = deepcopy(self.board)
        for idx, row in enumerate(self.board):
            for i, p in enumerate(row):
                if isinstance(p, Peca):
                    un = p.unicode
                else:
                    un = '\u25AF'
                data[idx][i] = un
        return data[::-1]
