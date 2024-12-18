import chess
import math
from collections import defaultdict

class IA_Ajedrez:
    def __init__(self, profundidad):
        self.profundidad = profundidad
        self.transposition_table = {}

    def evaluar_movimiento_rapido(self, tableroMagico, movimiento):
        """
        Heurística rápida para ordenar movimientos.
        Prioriza capturas y jaques.
        """
        tableroMagico.move(movimiento.from_square, movimiento.to_square)
        movimientos = tableroMagico.generar_movimientos()
        valor = heuristica_agresiva(tableroMagico, movimientos)
        return valor

    def generar_clave_tablero(self, tableroMagico):
        """
        Genera una clave única para el tablero actual.
        """
        return hash(tableroMagico.fen())

    def minimax_alfa_beta(self, tableroMagico, profundidad, alfa, beta, maximizando):
        """
        Minimax con poda alfa-beta, memorización y ordenamiento de movimientos.
        """
        if maximizando:
            tableroMagico.set_color(chess.BLACK)
        else:
            tableroMagico.set_color(chess.WHITE)

        movimientos = tableroMagico.generar_movimientos()

        clave = (self.generar_clave_tablero(tableroMagico), maximizando)
        if clave in self.transposition_table:
            return self.transposition_table[clave]

        if profundidad == 0 or tableroMagico.es_jaque_mate():
            #print("verdad?")
            evaluacion = heuristica_agresiva(tableroMagico.copy(),movimientos)
            self.transposition_table[clave] = (evaluacion, None)
            return evaluacion, None
        
        mejor_movimiento = None
        
        # if there are no legal moves, check for checkmate / stalemate
        if not movimientos:
            #print("verdad")
            if tableroMagico.es_jaque():
                if tableroMagico.result() == "1-0":
                    move_sequence.append(move)
                    return move_sequence, 1000000
                elif tableroMagico.result() == "0-1":
                    move_sequence.append(move)
                    return move_sequence, -1000000
            else:
                move_sequence.append(move)
                return move_sequence, 0

        # Ordenar movimientos
        movimientos_ordenados = sorted(
            movimientos,
            key=lambda mov: self.evaluar_movimiento_rapido(tableroMagico, mov),
            reverse=maximizando
        )

        if maximizando:
            max_eval = -math.inf
            contador = 0
            for movimiento in movimientos_ordenados:
                if tableroMagico.move(movimiento.from_square, movimiento.to_square):
                    evaluacion, _ = self.minimax_alfa_beta(tableroMagico.copy(), profundidad - 1, alfa, beta, False)
                    tableroMagico.pop()

                    if evaluacion > max_eval:
                        max_eval = evaluacion
                        mejor_movimiento = movimiento
                    alfa = max(alfa, evaluacion)
                    if beta <= alfa:
                        break  # Poda beta
                else:
                    contador += 1

            self.transposition_table[clave] = (max_eval, mejor_movimiento)
            #print(profundidad, len(movimientos_ordenados) - contador)
            return max_eval, mejor_movimiento
        else:
            min_eval = math.inf
            contador = 0
            for movimiento in movimientos_ordenados:
                if tableroMagico.move(movimiento.from_square, movimiento.to_square):
                    evaluacion, _ = self.minimax_alfa_beta(tableroMagico.copy(), profundidad - 1, alfa, beta, True)
                    tableroMagico.pop()

                    if evaluacion < min_eval:
                        min_eval = evaluacion
                        mejor_movimiento = movimiento
                    beta = min(beta, evaluacion)
                    if beta <= alfa:
                        break  # Poda alfa
                else:
                    contador += 1
            print(profundidad, len(movimientos_ordenados) - contador)
            self.transposition_table[clave] = (min_eval, mejor_movimiento)
            return min_eval, mejor_movimiento

    def mejor_movimiento(self, tableroMagico):
        """
        Encuentra el mejor movimiento para la IA.
        """
        _, movimiento = self.minimax_alfa_beta(tableroMagico.copy(), self.profundidad, -math.inf, math.inf, True)
        return movimiento

def heuristica(tableroMagico):
    """
    Evaluación agresiva para ajedrez de Alicia.
    """
    square_table = { 1: [
            0, 0, 0, 0, 0, 0, 0, 0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5, 5, 10, 25, 25, 10, 5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, -5, -10, 0, 0, -10, -5, 5,
            5, 10, 10, -20, -20, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0
        ],
        2: [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50,
        ],
        3: [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -20, -10, -10, -10, -10, -10, -10, -20,
        ],
        4: [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, 10, 10, 10, 10, 5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 5, 5, 0, 0, 0
        ],
        5: [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20
        ],
        6: [
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, 20, 0, 0, 0, 0, 20, 20,
            20, 30, 10, 0, 0, 10, 30, 20
        ]
    }

    piece_values = {
        # pawn
        1:100,
        # bishop
        2:310,
        # knight
        3:300,
        # rook
        4:500,
        # queen
        5:900,
        # king
        6:99999
    }

    def evaluar_tablero(tablero):
        score = 0
        # iterate through the pieces
        for i in range(1, 7):
            # eval white pieces
            w_squares = tablero.pieces(i, chess.WHITE)
            score += len(w_squares) * piece_values[i]
            for square in w_squares:
                score += square_table[i][-square]

            b_squares = tablero.pieces(i, chess.BLACK)
            score -= len(b_squares) * piece_values[i]
            for square in b_squares:
                score -= square_table[i][square]

        return score

    valor_negras = evaluar_tablero(tableroMagico.tablero1) + evaluar_tablero(tableroMagico.tablero2)
    #sincronizacion = len(tableroMagico.generar_movimientos())
    #jaques = 2 if tableroMagico.es_jaque() else 0

    return valor_negras



def heuristica_alicia(tableroMagico):
    """
    Heurística mejorada para Ajedrez de Alicia.
    Prioriza capturas, defensa y sincronización entre tableros.
    """
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 300,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    def evaluar_pieza(pieza, attackers_amigos, attackers_enemigos):
        """
        Evalúa el valor de una pieza considerando ataques y defensas.
        """
        valor_base = piece_values[pieza.piece_type]
        proteccion = len(attackers_amigos) * 10
        amenazas = len(attackers_enemigos) * 15
        return valor_base + proteccion - amenazas

    def evaluar_tablero(tablero):
        """
        Evalúa un solo tablero, considerando piezas, ataques y defensas.
        """
        score = 0
        for square in chess.SQUARES:
            pieza = tablero.piece_at(square)
            if pieza:
                attackers_amigos = tablero.attackers(pieza.color, square)
                attackers_enemigos = tablero.attackers(not pieza.color, square)
                if pieza.color == chess.WHITE:
                    score += evaluar_pieza(pieza, attackers_amigos, attackers_enemigos)
                else:
                    score -= evaluar_pieza(pieza, attackers_amigos, attackers_enemigos)
        return score

    # Evaluar ambos tableros
    valor_blancas = evaluar_tablero(tableroMagico.tablero1) + evaluar_tablero(tableroMagico.tablero2)

    # Bonus por capturas seguras y jaques en ambos tableros
    movimientos = tableroMagico.generar_movimientos()
    for movimiento in movimientos:
        if tableroMagico.is_capture(movimiento.from_square, movimiento.to_square):
            pieza_capturada = tableroMagico.piece_at(movimiento.to_square)
            if pieza_capturada:
                valor_captura = piece_values[pieza_capturada.piece_type]
                if len(tableroMagico.attackers(not pieza_capturada.color, movimiento)) == 0:
                    valor_blancas += valor_captura  # Captura segura
                else:
                    valor_blancas += valor_captura // 2  # Captura arriesgada

        if tableroMagico.es_jaque(movimiento):
            valor_blancas += 50  # Jaque en cualquier tablero

    # Ajuste por sincronización (menos movimientos posibles en uno de los tableros es malo)
    movimientos_totales = len(tableroMagico.generar_movimientos())
    if movimientos_totales < 10:  # Ejemplo: penalizar posiciones bloqueadas
        valor_blancas -= 50

    return valor_blancas


def heuristica_agresiva(tableroMagico, movimientos):
    """
    Heurística agresiva mejorada: favorece comer y defender.
    """
    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    
    score = 0

    for espacio in chess.SQUARES:
        pieza = tableroMagico.piece_at(espacio)
        if not pieza:
            continue
        if pieza.color == chess.WHITE:
            score += piece_values[pieza.piece_type]
            score += len(tableroMagico.attackers(chess.WHITE, espacio)) * 10  # Protección
            score -= len(tableroMagico.attackers(chess.BLACK, espacio)) * 15  # Amenazas
        else:
            score -= piece_values[pieza.piece_type]
            score -= len(tableroMagico.attackers(chess.BLACK, espacio)) * 10
            score += len(tableroMagico.attackers(chess.WHITE, espacio)) * 15

    # Bonus para jaques y capturas seguras
    # movimientos = tableroMagico.generar_movimientos()
    for movimiento in movimientos:
        if tableroMagico.is_capture(movimiento.from_square,movimiento.to_square):
            pieza_capturada = tableroMagico.piece_at(movimiento.to_square)
            if pieza_capturada:
                valor_captura = piece_values[pieza_capturada.piece_type]
                if len(tableroMagico.attackers(chess.BLACK, movimiento.to_square)) == 0:
                    score += valor_captura  # Captura segura
                else:
                    score += valor_captura // 2  # Captura arriesgada

        if tableroMagico.es_jaque(movimiento):
            score += 50  # Jaque

    return score
