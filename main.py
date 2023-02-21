import pygame

from gamestate import GameState
from gato import Gato
from rato import Rato
# Define algumas constantes
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
gato = Gato()
rato = Rato()


def load_images():
    pieces = ['wR','bp']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(
            f"pieces/{piece}.png"), (SQ_SIZE, SQ_SIZE))


def draw_board(screen):
    colors = [pygame.Color("grey"), pygame.Color("black")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(
                col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != '':
                screen.blit(IMAGES[piece], pygame.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_moves(screen, piece, row, col,color):
    if piece == 'wR':
        moves = gato.get_valid_moves(row, col)
    elif piece == 'bp':
        moves = rato.get_valid_moves(row, col)
    for move in moves:
        pygame.draw.circle(screen, pygame.Color(color), (
            move[1] * SQ_SIZE + SQ_SIZE//2, move[0] * SQ_SIZE + SQ_SIZE//2), SQ_SIZE//4)


def make_move(gs, piece, start_row, start_col, end_row, end_col):
    # Verifica se a jogada é válida
    if piece == 'wR':
        valid_moves = gato.get_valid_moves(start_row, start_col)
    elif piece == 'bp':
        valid_moves = rato.get_valid_moves(start_row, start_col)
        print("Movimentos validos do rato: ", valid_moves)
    if (end_row, end_col) not in valid_moves:
        return False

    # Realiza o movimento
    gs.board[end_row][end_col] = piece
    gs.board[start_row][start_col] = ''
    return True
def can_move(gs, piece):
    if piece == 'wR' and gs.white_to_move:
        return True
    elif piece == 'bp' and not gs.white_to_move:
        return True
    else:
        return False
def find_cat(gs):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if gs.board[row][col] == 'wR':
                return (row, col)
    return None

def verifica_vitoria_rato(gs):
    if find_cat(gs) == None:
        return True
    # Se o rato chegar na última linha, ele vence
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if gs.board[row][col] == 'bp':
                if row == 7:
                    return True
    return False

def verifica_vitoria_gato(gs):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if gs.board[row][col] == 'bp':
               return False
    return True



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo do Rato e Gato, Igor e Luisa")
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gs = GameState()
    load_images()

    running = True
    selected_piece = None
    while running:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = event.pos[1]//SQ_SIZE, event.pos[0]//SQ_SIZE
                piece = gs.board[row][col]
                if piece != '':
                    selected_piece = (piece, row, col)
                    print(selected_piece)
            elif event.type == pygame.MOUSEBUTTONUP:
                ## Se a posição após soltar o mouse for diferente da inicial, então é um movimento
                if selected_piece:
                    row, col = event.pos[1]//SQ_SIZE, event.pos[0]//SQ_SIZE
                    if can_move(gs, selected_piece[0]):
                        
                        if selected_piece[0] == 'wR':
                            futura_pos = (row,col)
                            if futura_pos in gato.get_valid_moves(selected_piece[1], selected_piece[2]):
                                if make_move(gs, selected_piece[0], selected_piece[1], selected_piece[2], row, col):
                                    gs.white_to_move = not gs.white_to_move

                        elif selected_piece[0] == 'bp':
                            futura_pos = (row, col)
                            #Se a posição futura for válida, então o rato pode se mover
                            if futura_pos in rato.get_valid_moves(selected_piece[1], selected_piece[2]):
                                if make_move(gs, selected_piece[0], selected_piece[1], selected_piece[2], row, col):
                                    gs.white_to_move = not gs.white_to_move
                        else:
                            print("Movimento inválido")
                                
                        gs.move_log.append((selected_piece[0], selected_piece[1], selected_piece[2], row, col))
                        ## Imprimir o histórico de movimentos
                        print(gs.move_log)
                    else:
                        print("Não é a sua vez")
                selected_piece = None
        draw_board(screen)
        draw_pieces(screen, gs.board)
        if selected_piece:
            if can_move(gs, selected_piece[0]):
                color = 'green'
            else:
                color = 'red'                
            highlight_moves(screen, selected_piece[0], selected_piece[1], selected_piece[2],color)

        if verifica_vitoria_rato(gs):
            # exibir uma tela verde
            screen.fill((0, 255, 0))  # preencher a tela com a cor verde
            font = pygame.font.Font(None, 36)  # carregar a fonte
            # renderizar o texto
            text = font.render("Vitória dos Ratos!", True, (255, 255, 255))
            # obter o retângulo do texto
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)  # desenhar o texto na janela
            pygame.display.flip()  # atualizar a janela
            pygame.time.wait(2000)  # esperar 2 segundos
            running = False  # sair do loop principal
        elif verifica_vitoria_gato(gs):
            # exibir uma tela vermelha
            screen.fill((255, 0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render("Vitória dos Gatos!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
        clock.tick(MAX_FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
