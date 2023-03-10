import time
import math
from gamestate import Board
from pieces.peca import Peca
from functools import wraps
from logger import Logger, BoardRepr
import random


logger = Logger()


def log_tree(func):
    """
    Decorator que registra a profundidade da árvore de busca em um arquivo, se a função de registro estiver ativada em um objeto Board.

    :param func: A função que está sendo decorada.
    :return: A função decorada que registra a profundidade da árvore de busca antes de chamar a função original.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        board: Board = args[0]
        if board.log:
            depth = args[1]
            write_to_file(board, depth)
        return func(*args, **kwargs)
    return wrapper


def write_to_file(board: Board, current_depth):
    global logger
    if board.depth == current_depth:
        logger.clear()
    board_repr = BoardRepr(board.unicode_array_repr(),
                           current_depth, board.evaluate())
    logger.append(board_repr)



@log_tree
def minimax_ab(board, depth, alpha, beta, max_player, save_move, data):
    """
    Executa o algoritmo Minimax com poda Alpha-Beta para determinar a melhor jogada possível para um jogador em um tabuleiro de xadrez.

    :param board: O objeto Board que representa o estado atual do tabuleiro.
    :param depth: A profundidade atual da árvore de busca.
    :param alpha: O valor atual de poda alpha.
    :param beta: O valor atual de poda beta.
    :param max_player: Um valor booleano que indica se o jogador atual é o jogador máximo ou mínimo.
    :param save_move: Um valor booleano que indica se os movimentos devem ser salvos para fins de depuração.
    :param data: Uma lista que armazena informações relevantes sobre o melhor movimento encontrado.
    :return: Uma lista contendo informações sobre o melhor movimento encontrado.
    """

    if depth == 0 or board.is_terminal():
        data[1] = board.evaluate()
        return data

    if max_player:
        max_eval = -math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], Peca) and board[i][j].color != board.get_player_color():
                    piece = board[i][j]
                    moves = piece.filter_moves(piece.get_moves(board), board)
                    for move in moves:
                        board.make_move(
                            piece, move[0], move[1], keep_history=True)
                        evaluation = minimax_ab(
                            board, depth - 1, alpha, beta, False, False, data)[1]
                        if save_move:
                            if evaluation >= max_eval:
                                if evaluation > data[1]:
                                    data.clear()
                                    data[1] = evaluation
                                    data[0] = [piece, move, evaluation]
                                elif evaluation == data[1]:
                                    data[0].append([piece, move, evaluation])
                        board.unmake_move(piece)
                        max_eval = max(max_eval, evaluation)
                        alpha = max(alpha, evaluation)
                        if beta <= alpha:
                            break
        return data
    else:
        min_eval = math.inf
        for i in range(8):
            for j in range(8):
                if isinstance(board[i][j], Peca) and board[i][j].color == board.get_player_color():
                    piece = board[i][j]
                    moves = piece.get_moves(board)
                    for move in moves:
                        board.make_move(
                            piece, move[0], move[1], keep_history=True)
                        evaluation = minimax_ab(
                            board, depth - 1, alpha, beta, True, False, data)[1]
                        board.unmake_move(piece)
                        min_eval = min(min_eval, evaluation)
                        beta = min(beta, evaluation)
                        if beta <= alpha:
                            break
        return data


""" def get_ai_move(board):
    
    A expressão [move for move in moves[0] if move[2] == best_score] usa uma compreensão de lista para criar uma lista com todos os movimentos em moves[0] que têm a pontuação best_score.
    A função random.choice é usada para escolher aleatoriamente um movimento dessa lista e armazená-lo na variável piece_and_move.

    moves = minimax_ab(board, board.depth, -math.inf, math.inf, True, True, [[], 0])
    if board.log:
        logger.write()
    # moves = [[pawn, move, move_score], [..], [..],[..], total_score]
    if len(moves[0]) == 0:
        return False
    best_score = max(moves[0], key=lambda x: x[2])[2]
    piece_and_move = random.choice(
        [move for move in moves[0] if move[2] == best_score])
    piece = piece_and_move[0]
    move = piece_and_move[1]
    if isinstance(piece, Peca) and len(move) > 0 and isinstance(move, tuple):
        board.make_move(piece, move[0], move[1])
    return True 
 """

def get_ai_move(board, max_time=5.0):
    
    """ 
    Retorna o próximo movimento sugerido pela busca minimax com poda alfa-beta com busca imperfeita em tempo real.

    Explicação:
    A função começa registrando o tempo atual e inicia um loop para iterar através das profundidades de busca a serem consideradas na busca minimax com poda alfa-beta. 
    Para cada profundidade, a função chama a função minimax_ab com os parâmetros necessários e salva o resultado em move_data. 
    Em seguida, o tempo decorrido desde o início da função é comparado com o tempo máximo permitido(max_time), e, se esse tempo for ultrapassado, o loop é interrompido.
    Depois disso, a função verifica se há movimentos possíveis e, se não houver, retorna False. 
    Se houver, a função seleciona o movimento com o maior score, e se houver empate, escolhe um aleatório entre as opções com o melhor score.

    Args:
    - board: instância da classe Board que representa o estado atual do tabuleiro.

    Returns:
    - bool: Retorna True se foi possível realizar um movimento ou False caso contrário.
     """
    start_time = time.time()
    moves = []
    for depth in range(1, board.depth+1):
        alpha = -math.inf
        beta = math.inf
        move_data = minimax_ab(board, depth, alpha, beta, True, True, [[], 0])
        moves.append(move_data)
        elapsed_time = time.time() - start_time
        if elapsed_time >= max_time:
            break
    if board.log:
        logger.write()
    flattened_moves = [move for sublist in moves for move in sublist[0]]
    if len(flattened_moves) == 0:
        return False
    best_score = max(flattened_moves, key=lambda x: x[2])[2]
    piece_and_move = random.choice(
        [move for move in flattened_moves if move[2] == best_score])
    piece = piece_and_move[0]
    # Exibir a escolha da IA

    move = piece_and_move[1]

    print("A IA escolheu a peça", piece, "para a posição",
          move, "com um score de", piece_and_move[2])
    print("Tempo gasto na busca:", elapsed_time, "segundos")
    if isinstance(piece, Peca) and len(move) > 0 and isinstance(move, tuple):
        board.make_move(piece, move[0], move[1])
    return True
