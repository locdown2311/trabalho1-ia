class Gato:
    def is_valid_move(self, row1, col1, row2, col2):
        return row1 == row2 or col1 == col2
    def get_valid_moves(self, row, col):
        moves = set()
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(row, col, r, c):
                    moves.add((r, c))
        return moves