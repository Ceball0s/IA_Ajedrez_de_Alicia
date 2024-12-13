import chess

# Definir un diccionario con el valor de cada tipo de pieza
pieza_valor = {
    chess.PAWN: 1,  # Peón
    chess.KNIGHT: 3,  # Caballo
    chess.BISHOP: 3,  # Alfil
    chess.ROOK: 5,  # Torre
    chess.QUEEN: 9,  # Reina
    chess.KING: 0,  # Rey (no tiene valor para puntaje, ya que no puede ser capturado)
}

def es_movimiento_rey_valido(origen, destino):
    """
    Verifica si el movimiento del rey es válido. El rey solo puede moverse a casillas adyacentes.

    :param origen: Coordenada de la casilla de origen (en formato de número de casilla, por ejemplo, 0 para 'a1').
    :param destino: Coordenada de la casilla de destino (en formato de número de casilla, por ejemplo, 9 para 'b1').
    :return: True si el movimiento es válido para el rey, False si no lo es.
    """
    # Obtenemos las filas y columnas a partir de la coordenada de casilla
    origen_fila, origen_columna = divmod(origen, 8)
    destino_fila, destino_columna = divmod(destino, 8)
    
    # El rey puede moverse a una casilla adyacente: filas y columnas difieren en a lo sumo 1
    if abs(origen_fila - destino_fila) <= 1 and abs(origen_columna - destino_columna) <= 1:
        return True
    return False

def se_puede_comer(fen, color):
    """
    Verifica si las blancas pueden comer en su turno.
    
    :param fen: FEN del tablero actual.
    :return: True si las blancas pueden comer, False en caso contrario.
    """
    # Crear el tablero a partir de la FEN
    tablero = chess.Board(fen)
    # Solo verificamos si es el turno de las blancas
    if tablero.turn == color:
        # Verificar todos los movimientos legales de las blancas
        for mov in tablero.legal_moves:
            #tablero.push(mov)
            # Verificar si el movimiento captura una pieza
            if tablero.is_capture(mov):
                print("puedo comer")
                return True  # Si se captura una pieza, las blancas pueden comer
            #tablero.pop() 
    print("no puedo comer")
    return False  # Si no hay capturas, las blancas no pueden comer



def verificar_movimiento_pierde_gana(fen, movimiento):
    """
    Verifica si un movimiento es válido en la variante 'Pierde-Gana'.
    La regla es que el movimiento solo es válido si captura una pieza.

    :param fen: FEN del tablero actual.
    :param movimiento: Movimiento en formato UCI (ej. 'e2e4').
    :return: Una tupla con (es_valido, nueva_fen) donde es_valido es un booleano y
             nueva_fen es la FEN actualizada tras el movimiento (si es válido).
    """
    def funcion_retorno():
        score_blancas, score_negras = contar_fichas(fen)
        return tablero.fen(), score_blancas, score_negras

    # Crear el tablero a partir de la FEN
    tablero = chess.Board(fen)

    # Intentar hacer el movimiento
    try:
        mov = chess.Move.from_uci(movimiento)
        if mov in tablero.legal_moves or tablero.piece_at(mov.from_square).piece_type == chess.KING:
            # Verificar si el movimiento ha capturado una pieza
            if tablero.is_capture(mov):
                # Realiza el movimiento en el tablero
                tablero.push(mov)
                # Si ha capturado una pieza, el movimiento es válido
                return funcion_retorno()
            else:
                # Verificar si el movimiento es de un rey
                if tablero.piece_at(mov.from_square).piece_type == chess.KING:
                    # El rey se mueve una casilla en cualquier dirección, pero solo puede
                    # moverse a una casilla vacía o que esté ocupada por una pieza enemiga
                    destino = mov.to_square
                    pieza_destino = tablero.piece_at(destino)
                    
                    # Verificar si la casilla de destino es válida
                    if (pieza_destino is None or pieza_destino.color != tablero.turn) and es_movimiento_rey_valido(mov.from_square,destino):
                        # Realiza el movimiento en el tablero
                        tablero.push(mov)
                        return funcion_retorno()
                    else:
                        return funcion_retorno()
                if se_puede_comer(fen,chess.WHITE):
                    return funcion_retorno()
                tablero.push(mov)
                # EL jugador no podia comer
                return funcion_retorno()
        else:
            # Si el movimiento no es legal, retornar la FEN original
            return funcion_retorno()
        
    except ValueError:
        # Si el formato del movimiento no es válido, retornar la FEN original
        return funcion_retorno()




def contar_fichas(fen):
    """
    Cuenta las piezas de cada jugador y calcula su puntaje total.

    :param tablero: El tablero de ajedrez representado como un objeto `chess.Board`.
    :return: Una tupla con los puntajes de las blancas y negras (score_blancas, score_negras).
    """
    score_blancas = 0
    score_negras = 0
    piezas_blancas = 0
    piezas_negras = 0
    score_maximo_normal = 39

    tablero = chess.Board(fen)
    
    for square in chess.SQUARES:  # Recorremos todas las casillas del tablero
        pieza = tablero.piece_at(square)
        
        if pieza is not None:  # Si la casilla tiene una pieza
            valor = pieza_valor.get(pieza.piece_type, 0)  # Obtener el valor de la pieza
            
            if pieza.color == chess.WHITE:
                score_blancas += valor
                piezas_blancas += 1
            elif pieza.color == chess.BLACK:
                score_negras += valor
                piezas_negras += 1

    return score_maximo_normal-score_blancas, score_maximo_normal-score_negras


def generate_legal_moves(board):
    """
    Genera movimientos legales con prioridad para capturas obligatorias.
    """
    if all(not board.is_capture(x) for x in board.legal_moves):
        return board.legal_moves
    capture_moves = [move for move in board.legal_moves if board.is_capture(move)]
    return capture_moves
