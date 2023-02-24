from pieces.peca import Peca

class Rato(Peca):
    def __init__(self, color, x, y, unicode):
        super().__init__(color, x, y, unicode)
        self.moved = True
    def get_moves(self, board):
        """
        Retorna uma lista de movimentos possíveis para o rato.

        Args:
            board (objeto Board): o objeto de tabuleiro que representa o estado atual do jogo.

        Returns:
            list: uma lista de tuplas que representam os movimentos possíveis no tabuleiro, 
                onde cada tupla tem a forma (linha_final, coluna_final).
        """
        moves = []
        if board.game_mode == 0 and self.color == 'white' or board.game_mode == 1 and self.color == 'black':
            direction = 1
        else:
            direction = -1
        x = self.x + direction
        if board.has_empty_block(x, self.y):
            moves.append((x, self.y))
            if self.moved is False and board.has_empty_block(x + direction, self.y):
                moves.append((x + direction, self.y))
        if board.is_valid_move(x, self.y - 1):
            if board.has_opponent(self, x, self.y - 1):
                moves.append((x, self.y - 1))
        if board.is_valid_move(self.x + direction, self.y + 1):
            if board.has_opponent(self, x, self.y + 1):
                moves.append((x, self.y + 1))
        return moves

    def get_score(self):
        return 3
