import chess
import math

class IA_Ajedrez:
    def __init__(self, profundidad):
        self.profundidad = profundidad
    
    def minimax(self, tableroMagico, profundidad, maximizando):
        """
        Implementación del algoritmo Minimax con recursión.
        """
        if profundidad == 0 or tableroMagico.es_jaque_mate():
            return evaluar_posicion_agresiva(tableroMagico.copy()), None

        if maximizando:
            max_eval = -math.inf
            mejor_movimiento = None
            for movimiento in tableroMagico.generar_movimientos():
                tableroMagico.move(movimiento.from_square, movimiento.to_square)
                evaluacion, _ = self.minimax(tableroMagico.copy(), profundidad - 1, False)
                tableroMagico.pop()
                if evaluacion > max_eval:
                    max_eval = evaluacion
                    mejor_movimiento = movimiento
            return max_eval, mejor_movimiento
        else:
            min_eval = math.inf
            mejor_movimiento = None
            for movimiento in tableroMagico.generar_movimientos():
                tableroMagico.move(movimiento.from_square, movimiento.to_square)
                evaluacion, _ = self.minimax(tableroMagico.copy(), profundidad - 1, True)
                tableroMagico.pop()
                if evaluacion < min_eval:
                    min_eval = evaluacion
                    mejor_movimiento = movimiento
            return min_eval, mejor_movimiento

    def mejor_movimiento(self, tableroMagico):
        """
        Encuentra el mejor movimiento para la IA.
        """
        _, movimiento = self.minimax(tableroMagico.copy(), self.profundidad, True)
        return movimiento

def evaluar_posicion_agresiva(tableroMagico):
    """
    Evaluación agresiva para ajedrez de Alicia.
    Combina control, presión al rey enemigo y sincronización entre tableros.
    """
    valor_piezas = {
        chess.PAWN: 1,
        chess.KNIGHT: 3.5,  # Los caballos tienen ventaja estratégica en sincronización
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # El rey no tiene valor directo
    }

    def evaluar_tablero(tablero, color_aliado):
        valor = 0
        for square in chess.SQUARES:
            pieza = tablero.piece_at(square)
            if pieza:
                # Valorar la pieza
                factor = 1 if pieza.color == color_aliado else -1
                valor += valor_piezas[pieza.piece_type] * factor

                # Agregar valor por control agresivo
                if pieza.color == chess.BLACK:
                    valor += len(tablero.attacks(square)) * 0.1  # Más control es mejor

                # Penalizar peones bloqueados
                if pieza.piece_type == chess.PAWN and tablero.is_pinned(pieza.color, square):
                    valor -= 0.5

        return valor

    # Valor total combinado de ambos tableros
    valor_negras = evaluar_tablero(tableroMagico.tablero1, chess.BLACK) + evaluar_tablero(tableroMagico.tablero2, chess.BLACK)
    valor_blancas = evaluar_tablero(tableroMagico.tablero1, chess.WHITE) + evaluar_tablero(tableroMagico.tablero2, chess.WHITE)

    # Favorecer sincronización y jaques
    sincronizacion = len(tableroMagico.generar_movimientos())
    jaques = 2 if tableroMagico.es_jaque() else 0

    return valor_negras - valor_blancas + sincronizacion * 0.5 + jaques
