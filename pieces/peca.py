class Peca:

    # history is used to keep data, so board.unmake_move() works properly.
    eaten_pieces_history = []
    has_moved_history = []
    position_history = []

    def __init__(self, color, x, y, unicode):
        self.moved = False
        self.color = color
        self.x = x
        self.y = y
        self.type = self.__class__.__name__
        self.unicode = unicode

    def filter_moves(self, moves, board):
        final_moves = moves[:]
        for move in moves:
            board.make_move(self, move[0], move[1], keep_history=True)
            board.unmake_move(self)
        return final_moves

    def get_moves(self, board):
        pass

    def get_last_eaten(self):
        return self.eaten_pieces_history.pop()

    def set_last_eaten(self, piece):
        self.eaten_pieces_history.append(piece)

    def set_position(self, x, y, keep_history):
        if keep_history:
            self.position_history.append(self.x)
            self.position_history.append(self.y)
            self.has_moved_history.append(self.moved)
        self.x = x
        self.y = y
        self.moved = True

    def set_old_position(self):
        position_y = self.position_history.pop()
        position_x = self.position_history.pop()
        self.y = position_y
        self.x = position_x
        self.moved = self.has_moved_history.pop()

    def get_score(self):
        return 0

    def __repr__(self):
        return '{}: {}|{},{}'.format(self.type, self.color, self.x, self.y)

