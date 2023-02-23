import visual
from gamestate import *


if __name__ == '__main__':
    # game_mode == 0: Brancas na parte inferior / 1: Pretas na parte inferior
    board = Board(game_mode=0, ai=True, depth=5, log=True)
    
    visual.initialize()
    board.place_pieces()
    visual.draw_background(board)
    keep_playing = visual.start(board)
