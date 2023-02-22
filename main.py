import visual
from gamestate import *


if __name__ == '__main__':
    # game_mode == 0: whites down / 1: blacks down
    board = Board(game_mode=0, ai=True, depth=5, log=True)
    
    visual.initialize()
    board.place_pieces()
    visual.draw_background(board)
    keep_playing = visual.start(board)
