from pieces.peca import Peca
import operator
class Gato(Peca):
    def get_moves(self, board):
        moves = []
        moves += self.get_vertical_moves(board)
        moves += self.get_horizontal_moves(board)
        return moves

    def get_vertical_moves(self, board):
        """
        Retorna uma lista de movimentos possíveis para a peça vertical no tabuleiro especificado.

        Args:
        - self: a peça vertical para a qual desejamos gerar movimentos.
        - board: o tabuleiro no qual a peça está atualmente posicionada.

        Returns:
        - Uma lista de tuplas (x, y) representando as coordenadas de cada movimento possível.
        Cada movimento é uma posição vertical adjacente à posição atual da peça no tabuleiro,
        ou a posição de uma peça adversária que pode ser capturada em um movimento.

        O método itera duas vezes em um loop for para gerar movimentos possíveis para a peça:
        - A primeira iteração (usando a função `operator.add`) verifica os movimentos possíveis acima da posição atual da peça.
        - A segunda iteração (usando a função `operator.sub`) verifica os movimentos possíveis abaixo da posição atual da peça.
        Em cada iteração, o loop verifica se o movimento é válido de acordo com as regras do jogo, e adiciona o movimento à lista `moves`
        se ele satisfaz essas condições.
        A lista de movimentos resultante é então retornada.
        """
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
        """
        Retorna uma lista de movimentos possíveis para a peça horizontal no tabuleiro especificado.

        Args:
        - self: a peça horizontal para a qual desejamos gerar movimentos.
        - board: o tabuleiro no qual a peça está atualmente posicionada.

        Returns:
        - Uma lista de tuplas (x, y) representando as coordenadas de cada movimento possível.
        Cada movimento é uma posição horizontal adjacente à posição atual da peça no tabuleiro,
        ou a posição de uma peça adversária que pode ser capturada em um movimento.

        O método itera duas vezes em um loop for para gerar movimentos possíveis para a peça:
        - A primeira iteração (usando a função `operator.add`) verifica os movimentos possíveis à direita da posição atual da peça.
        - A segunda iteração (usando a função `operator.sub`) verifica os movimentos possíveis à esquerda da posição atual da peça.
        Em cada iteração, o loop verifica se o movimento é válido de acordo com as regras do jogo, e adiciona o movimento à lista `moves`
        se ele satisfaz essas condições.
        A lista de movimentos resultante é então retornada.
        """
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
