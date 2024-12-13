import chess
from Proyecto.reglas_tablero import generate_legal_moves

def evaluate_board(board):
    """
    Evalúa el tablero para la variante Pierde Gana.
    Un valor más bajo es mejor para el jugador actual (menos piezas propias).
    """
    # my_pieces = len(board.piece_map())  # Total de piezas en el tablero
    # return my_pieces
    black_pieces = sum(1 for piece in board.piece_map().values() if piece.color == chess.BLACK) 
    return black_pieces

def minimax(board, depth, is_maximizing, alpha, beta):
    """
    Implementación del algoritmo Minimax con poda alfa-beta.
    """
    if depth == 0:
        return evaluate_board(board)
    
    legal_moves = generate_legal_moves(board)
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, alpha, beta)
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
    best_value = float('inf')  # Buscamos minimizar la evaluación
    for move in generate_legal_moves(board):
        board.push(move)
        board_value = minimax(board, depth - 1, True, float('-inf'), float('inf'))
        board.pop()
        if board_value < best_value:
            best_value = board_value
            best_move = move
    return best_move
