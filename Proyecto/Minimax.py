import chess

def evaluate_board(board, is_white):
    """
    Evalúa el tablero para favorecer una estrategia agresiva.
    :param board: El estado actual del tablero.
    :param is_white: True si la IA juega como blancas, False si juega como negras.
    """
    score = 0
    tablero1, tablero2 = board.get_tableros()  # Obtener los tableros de Alicia

    # Valores de piezas
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 10000  # Alto valor para priorizar el rey
    }

    capture_bonus = 2.0  # Incentiva capturar piezas del oponente
    safety_penalty = 0.8  # Penaliza piezas propias en peligro
    safety_bonus = 0.5    # Premia piezas propias seguras

    # 1. Revisar jaque mate
    if board.es_jaque_mate():
        return -10000 if board.turn == is_white else 10000

    # 2. Revisar jaque
    if board.es_jaque():
        score -= 100 if board.turn == is_white else 100

    # 3. Evaluar piezas en ambos tableros
    for tablero in [tablero1, tablero2]:
        for square in chess.SQUARES:
            piece = tablero.piece_at(square)
            if piece:
                # Obtener el valor base de la pieza
                value = piece_values.get(piece.piece_type, 0)

                # Ajustar puntuación según el color de la IA
                if piece.color == is_white:
                    score += value  # Premia piezas propias
                    is_safe = not tablero.is_attacked_by(not piece.color, square)
                    if is_safe:
                        score += value * safety_bonus
                    else:
                        score -= value * safety_penalty
                else:
                    score -= value  # Penaliza piezas enemigas
                    is_safe = not tablero.is_attacked_by(not piece.color, square)
                    if not is_safe:
                        score += value * capture_bonus

            # Contar atacantes para cada casilla
            white_attackers = len(tablero.attackers(chess.WHITE, square))
            black_attackers = len(tablero.attackers(chess.BLACK, square))

            if is_white:
                score += white_attackers * capture_bonus
                score -= black_attackers * capture_bonus
            else:
                score -= white_attackers * capture_bonus
                score += black_attackers * capture_bonus

    return score


def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Implementación del algoritmo Minimax con poda alfa-beta.
    """
    if depth == 0:
        return evaluate_board(board.copy(),True)
    
    if is_maximizing:
        board.set_color(chess.BLACK)
        legal_moves = board.generar_movimientos()
        max_eval = float('-inf')
        for move in legal_moves:
            if not board.move(move.from_square,move.to_square):
                print("no")
            eval = minimax(board.copy(), depth - 1, False, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        board.set_color(chess.WHITE)
        legal_moves = board.generar_movimientos()
        min_eval = float('inf')
        for move in legal_moves:
            #board.move(move.from_square,move.to_square)
            if not board.move(move.from_square,move.to_square):     
                print("no")
            eval = minimax(board.copy(), depth - 1, True, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    """
    Encuentra el mejor movimiento para la variante Pierde Gana.
    """
    best_move = None
    best_value = float('-inf')  # Buscamos maximizar la evaluación
    lista_movimiento = board.generar_movimientos()
    for move in lista_movimiento:
        board.move(move.from_square,move.to_square)
        board_value = minimax(board.copy(), depth - 1, False, float('-inf'), float('inf'))
        board.pop()
        if board_value > best_value:
            best_value = board_value
            best_move = move
    return best_move
