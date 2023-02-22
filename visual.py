import pygame
from pieces.peca import Peca
from inteligencia import get_ai_move


whiteGato = pygame.image.load('pieces_assets/wR.png')
whiteGato = pygame.transform.scale(whiteGato, (75, 75))
blackRato = pygame.image.load('pieces_assets/bp.png')
blackRato = pygame.transform.scale(blackRato, (75, 75))
bloco_escuro = pygame.image.load('pieces_assets/marrom_escuro.png')
bloco_claro = pygame.image.load('pieces_assets/marrom_claro.png')
bloco_escuro = pygame.transform.scale(bloco_escuro, (75, 75))
bloco_claro = pygame.transform.scale(bloco_claro, (75, 75))

previsao = pygame.image.load('pieces_assets/previsao.png')
previsao = pygame.transform.scale(previsao, (75, 75))

screen = None
pygame.font.init()
font = pygame.font.SysFont('Arial', 22)


def initialize():
    """
    Função que inicializa o Pygame e define a janela do jogo.

    Inicializa o módulo Pygame e define o título da janela do jogo. Em seguida,
    cria uma janela com as dimensões de 600x650 pixels e preenche com a cor preta.

    Parâmetros:
    Nenhum.

    Retorno:
    Nenhum.
    """
    global screen
    pygame.init()
    pygame.display.set_caption('Jogo diferenciado de Igor e Luisa')
    screen = pygame.display.set_mode((600, 650))
    screen.fill((0, 0, 0))


def draw_background(board):
    """
    Desenha o fundo do tabuleiro e as peças nele contidas.

    Parâmetros:
    board (list): uma lista que representa o estado atual do tabuleiro.

    Retorno:
    None
    """
    block_x = 0
    for i in range(4):
        block_y = 0
        for j in range(4):
            screen.blit(bloco_claro, (block_x, block_y))
            screen.blit(bloco_escuro, (block_x + 75, block_y))
            screen.blit(bloco_claro, (block_x + 75, block_y + 75))
            screen.blit(bloco_escuro, (block_x, block_y + 75))
            block_y += 150
        block_x += 150
    step_x = 0
    step_y = pygame.display.get_surface().get_size()[0] - 75
    for i in range(8):
        for j in range(8):
            if isinstance(board[i][j], Peca):
                obj = globals()[f'{board[i][j].color}{board[i][j].type}']
                screen.blit(obj, (step_x, step_y))
            step_x += 75
        step_x = 0
        step_y -= 75
    pygame.display.update()


def draw_text(text):
    """
    Desenha um texto na parte inferior da tela.

    Parâmetros:
    text (str): o texto a ser exibido na tela.

    Retorno:
    None
    """
    s = pygame.Surface((400, 50))
    s.fill((0, 0, 0))
    screen.blit(s, (100, 600))
    text_surface = font.render(text, True, (100, 237, 237))
    x = 230
    screen.blit(text_surface, (x, 600))
    pygame.display.update()


def start(board):
    """
    Inicia o jogo com um tabuleiro e executa o loop principal do jogo.

    Parâmetros:
    board (Tabuleiro): o tabuleiro do jogo.

    Retorno:
    None
    """
    global screen
    possible_piece_moves = []
    running = True
    visible_moves = False
    dimensions = pygame.display.get_surface().get_size()
    game_over = False
    piece = None
    if board.game_mode == 1 and board.ai:
        get_ai_move(board)
        draw_background(board)
    while running:
        if game_over:
            draw_text(game_over_txt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x = 7 - pygame.mouse.get_pos()[1] // 75
                y = pygame.mouse.get_pos()[0] // 75
                if isinstance(board[x][y], Peca) and (board.get_player_color() == board[x][y].color or not board.ai) and (x, y) not in possible_piece_moves:
                    piece = board[x][y]
                    moves = piece.filter_moves(piece.get_moves(board), board)
                    move_positions = []
                    possible_piece_moves = []
                    for move in moves:
                        move_positions.append(
                            (dimensions[0] - (8 - move[1]) * 75, dimensions[1] - move[0] * 75 - 125))
                        move_x = 7 - move_positions[-1][1] // 75
                        move_y = move_positions[-1][0] // 75
                        possible_piece_moves.append((move_x, move_y))
                    if visible_moves:
                        draw_background(board)
                        visible_moves = False
                    for move in move_positions:
                        visible_moves = True
                        screen.blit(previsao, (move[0], move[1]))
                        pygame.display.update()
                else:
                    clicked_move = (x, y)
                    try:
                        if clicked_move in possible_piece_moves:
                            board.make_move(piece, x, y)
                            possible_piece_moves.clear()
                            draw_background(board)
                            if board.ai:
                                get_ai_move(board)
                                draw_background(board)

                        if board.white_won():
                            game_over = True
                            game_over_txt = 'Gato ganhou!'
                        elif board.black_won():
                            game_over = True
                            game_over_txt = 'Rato ganhou!'
                    except UnboundLocalError:
                        pass
