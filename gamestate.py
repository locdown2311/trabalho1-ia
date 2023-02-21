class GameState:
    def __init__(self):
        # Representação do tabuleiro
        self.board = [
            ['', '', '', '', '', '', '', ''],
            ['bp', 'bp', 'bp', '', '', 'bp', 'bp', 'bp'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', 'wR', '', '', '', ''],
            ['', '', '', '', '', '', '', '']
        ]
        self.white_to_move = True

        #Pilha de movimentos
        self.move_log = []

        self.scores = {'bp': -1, 'wR': 6}

    def is_valid_position(self,row, col):
        return 0 <= row <= 7 and 0 <= col <= 7
