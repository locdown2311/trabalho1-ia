from pieces.peca import Peca
import operator
class Gato(Peca):
    def get_moves(self, board):
        moves = []
        moves += self.get_vertical_moves(board)
        moves += self.get_horizontal_moves(board)
        return moves

    def get_vertical_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                x = op(self.x, i)
                if not board.is_valid_move(x, self.y) or board.has_friend(self, x, self.y):
                    break
                if board.has_empty_block(x, self.y):
                    moves.append((x, self.y))
                if board.has_opponent(self, x, self.y):
                    moves.append((x, self.y))
                    break
        return moves

    def get_horizontal_moves(self, board):
        moves = []
        for op in [operator.add, operator.sub]:
            for i in range(1, 9):
                y = op(self.y, i)
                if not board.is_valid_move(self.x, y) or board.has_friend(self, self.x, y):
                    break
                if board.has_empty_block(self.x, y):
                    moves.append((self.x, y))
                if board.has_opponent(self, self.x, y):
                    moves.append((self.x, y))
                    break
        return moves

    def get_score(self):
        return 5
