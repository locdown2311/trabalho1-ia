class Rato:
    
    def is_valid_move(self, row1, col1, row2, col2):
        direction = 1  # peão preto move para baixo
        if row1 + direction == row2 and col1 == col2:  # avanço de uma casa
            return True
        elif row1 + direction == row2 and abs(col2 - col1) == 1:  # captura diagonal
            return True
        else:
            return False

    

    def get_valid_moves(self, row, col):
        moves = set()
        for r in range(8):
            for c in range(8):
                if self.is_valid_move(row, col, r, c):
                    moves.add((r, c))
        if len(moves) > 0:
            if moves.__iter__().__next__()[0] == row:
                moves = {move for move in moves if move[0] == row}
            else:
                moves = {move for move in moves if move[0] != row}
        return moves
