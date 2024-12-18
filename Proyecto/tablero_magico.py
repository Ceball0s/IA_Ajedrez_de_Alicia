import chess

class tablero_magico:
    def __init__(self,tablero1,tablero2,color):
        self.tablero1 = tablero1
        self.tablero2 = tablero2
        self.color = color
        self.tablero1.turn = color
        self.tablero2.turn = color
        self.tablero1_antes = tablero1.copy()
        self.tablero2_antes = tablero2.copy()
        self.promover_peones()
        self.square_table = { 1: [
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

        self.piece_values = {
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

    def set_color(self,color):
        self.color = color
        self.tablero1.turn = color
        self.tablero2.turn = color

    def fen(self):
        return self.tablero1.fen() + " " + self.tablero2.fen()

    def copy(self):
        """
        Crea una copia profunda del objeto tablero_magico.
        """
        nuevo_tablero1 = self.tablero1.copy()  # Copia del tablero 1
        nuevo_tablero2 = self.tablero2.copy()  # Copia del tablero 2
        nuevo_color = self.color  # Color actual del turno

        # Crear un nuevo objeto `tablero_magico` con los tableros copiados
        return tablero_magico(nuevo_tablero1, nuevo_tablero2, nuevo_color)

    def casilla_ocupada(self, tablero, square_index):
        piece = tablero.piece_at(square_index)
        if piece:
            return True
        else:
            return False


    # verifica general
    def verificar_movimiento(self, original, destino, tabla_original, tabla_destino): 
        def proxima_posicion_es_jaque(tabla_des, piece_tablero1):
            tabla_des.set_piece_at(original_dix, piece_tablero1)
            if tabla_des.is_check():
                return True
            else:
                return False
    
        # despues del movimiento sigue abiendo jaque en el mismo tablero entonces el movimeinto es invalido
        def movimiento_anula_jaque(tabla1, tabla2):
            print("calculando")
            if tabla1.is_check():
                tabla1.remove_piece_at(original_dix)
                tabla1.remove_piece_at(destino_idx)
                tabla2.set_piece_at(destino_idx, piece_tablero1)
                if tabla1.is_check():
                    return False
            if tabla2.is_check():
                tabla1.remove_piece_at(original_dix)
                tabla1.remove_piece_at(destino_idx)
                tabla2.set_piece_at(destino_idx, piece_tablero1)
                if tabla2.is_check():
                    return False
            return True

        piece_tablero1 = tabla_original.piece_at(original)
        original = chess.square_name(original)
        destino = chess.square_name(destino)
        mov = chess.Move.from_uci(original + destino)
        # Convierte 'destino' a su índice numérico usando chess.parse_square
        destino_idx = chess.parse_square(destino)
        original_dix = chess.parse_square(original)
        
        # Si el peón llega a la octava fila (para blancas) o a la primera fila (para negras), se promociona
        if (tabla_original.piece_at(mov.from_square).piece_type == chess.PAWN and
            (chess.square_rank(destino_idx) == 7 if tabla_original.piece_at(mov.from_square).color == chess.WHITE else chess.square_rank(destino_idx) == 0)):
            # Creamos el movimiento de promoción, transformando el peón en reina
            promotion_move = chess.Move(mov.from_square, mov.to_square, promotion=chess.QUEEN)
            if promotion_move in tabla_original.legal_moves and not self.casilla_ocupada(tabla_destino, chess.parse_square(destino)):
                # print("Peón promovido a reina")
                return True
            else:
                # print("Movimiento de promoción no permitido")
                return False

        if not mov in tabla_original.legal_moves:
            # Permitimos que el rey se mueva solo si está en una casilla adyacente (como es su movimiento estándar)
            if piece_tablero1.piece_type == chess.KING and not proxima_posicion_es_jaque(tabla_destino.copy(), piece_tablero1):
                # El rey solo puede moverse a una casilla adyacente
                fila_original, col_original = chess.square_rank(original), chess.square_file(original)
                fila_destino, col_destino = chess.square_rank(destino), chess.square_file(destino)

                # Verificamos si el movimiento es adyacente (movimiento estándar del rey)
                if not abs(fila_original - fila_destino) <= 1 and abs(col_original - col_destino) <= 1:
                    return False
            else:
                return False
        elif self.casilla_ocupada(tabla_destino, chess.parse_square(destino)):
            return False
        elif piece_tablero1.piece_type == chess.KING and proxima_posicion_es_jaque(tabla_destino.copy(), piece_tablero1):
            return False
        elif (tabla_original.is_check() or tabla_destino.is_check()) and not movimiento_anula_jaque(tabla_original.copy(),tabla_destino.copy()):
            return False
        else:
            return True

    def move(self, origen, destino):
        # tabla_original, tabla_destino = self.tabla_original_destino(origen)
        #square = origen)  # Convierte "e4" a un índice (28)
        # Verificar si hay una pieza en la casilla
        piece_tablero1 = self.tablero1.piece_at(origen)
        piece_tablero2 = self.tablero2.piece_at(origen)
        # self.tablero1.turn = self.color
        # self.tablero2.turn = self.color
        if piece_tablero1:
            if self.verificar_movimiento(origen, destino, self.tablero1, self.tablero2):
                self.tablero1_antes = self.tablero1.copy()
                self.tablero2_antes = self.tablero2.copy()
                self.tablero1.remove_piece_at(origen)
                self.tablero1.remove_piece_at(destino)
                self.tablero2.set_piece_at(destino, piece_tablero1)
                self.promover_peones()
                self.tablero1.turn = not self.tablero1.turn
                self.tablero2.turn = not self.tablero2.turn
                self.color = not self.color
                return True
        elif piece_tablero2:
            if self.verificar_movimiento(origen, destino, self.tablero2, self.tablero1):
                self.tablero1_antes = self.tablero1.copy()
                self.tablero2_antes = self.tablero2.copy()
                self.tablero2.remove_piece_at(origen)
                self.tablero2.remove_piece_at(destino)
                self.tablero1.set_piece_at(destino, piece_tablero2)
                self.promover_peones()
                self.tablero1.turn = not self.tablero1.turn
                self.tablero2.turn = not self.tablero2.turn
                self.color = not self.color
                return True
        return False   

    def generar_movimientos(self):
        lista_movimiento = []

        # Movimientos del tablero1
        for move in self.tablero1.legal_moves:
            if not self.casilla_ocupada(self.tablero2, move.to_square):
                lista_movimiento.append(move)

        # Movimientos del tablero2
        for move in self.tablero2.legal_moves:
            if not self.casilla_ocupada(self.tablero1, move.to_square):
                lista_movimiento.append(move)

        return lista_movimiento

    def is_captis_captureure(self, origen, destino):
        # tabla_original, tabla_destino = self.tabla_original_destino(origen)
        #square = origen)  # Convierte "e4" a un índice (28)
        # Verificar si hay una pieza en la casilla
        piece_tablero1 = self.tablero1.piece_at(origen)
        piece_tablero2 = self.tablero2.piece_at(origen)
        if piece_tablero1:
            return self.verificar_captura(origen, destino, self.tablero1, self.tablero2)
        elif piece_tablero2:
            return self.verificar_captura(origen, destino, self.tablero2, self.tablero1)
      
    def verificar_captura(self, original, destino, tabla_original, tabla_destino):
        original = chess.square_name(original)
        destino = chess.square_name(destino)
        mov = chess.Move.from_uci(original + destino)
        if mov in tabla_original.legal_moves and tabla_original.is_capture(mov) and  not self.casilla_ocupada(tabla_destino, chess.parse_square(destino)):
            return True
        else:
            return False
     
    def piece_at(self,destino):
        pieza = self.tablero1.piece_at(destino)
        if not pieza:
            return self.tablero2.piece_at(destino)
        else:
            return pieza

    def attackers(self, color, movimiento):
        #ficha_actual = movimiento.from_square
        pieza = self.tablero1.piece_at(movimiento)
        if not pieza:
            return self.tablero2.attackers(color,movimiento)
        else:
            return self.tablero1.attackers(color,movimiento)

    def get_tableros(self):
        return self.tablero1.copy(),self.tablero2.copy()

    def pop(self):
        self.tablero1 = self.tablero1_antes.copy()
        self.tablero2 = self.tablero2_antes.copy()
        # self.tablero1.turn = not self.tablero1.turn
        # self.tablero2.turn = not self.tablero2.turn
        self.color = not self.color

        
    def result(self):
        if "1" in self.tablero1.result():
            return self.tablero1.result()
        return self.tablero2.result()

    

    def promover_peones(self):
        """Recorre ambos tableros y promueve los peones que estén en la última fila (para blancas) o la primera fila (para negras)."""
        # Recorrer tablero1
        for square in range(64):
            pieza = self.tablero1.piece_at(square)
            if pieza and pieza.piece_type == chess.PAWN:
                if (pieza.color == chess.WHITE and chess.square_rank(square) == 7) or \
                (pieza.color == chess.BLACK and chess.square_rank(square) == 0):
                    # Promover el peón a reina
                    self.tablero1.set_piece_at(square, chess.Piece(chess.QUEEN, pieza.color))
                    #print(f"Peón en {chess.square_name(square)} promovido a Reina en tablero1")

        # Recorrer tablero2
        for square in range(64):
            pieza = self.tablero2.piece_at(square)
            if pieza and pieza.piece_type == chess.PAWN:
                if (pieza.color == chess.WHITE and chess.square_rank(square) == 7) or \
                (pieza.color == chess.BLACK and chess.square_rank(square) == 0):
                    # Promover el peón a reina
                    self.tablero2.set_piece_at(square, chess.Piece(chess.QUEEN, pieza.color))
                    # print(f"Peón en {chess.square_name(square)} promovido a Reina en tablero2")

    def es_jaque(self):
        """
        Determina si el jugador contrario está en jaque mate.
        Retorna True si hay jaque mate, False en caso contrario.
        """
        # Cambiar el turno temporalmente para analizar al oponente
        color_oponente = not self.color
        #self.tablero1.turn = color_oponente
        #self.tablero2.turn = color_oponente

        # Verificar si el rey del oponente está en jaque en cualquiera de los tableros
        return self.tablero1.is_check() or self.tablero2.is_check()

    def es_jaque(self, movimiento):
        """
        Determina si el jugador contrario está en jaque mate.
        Retorna True si hay jaque mate, False en caso contrario.
        """
        # Cambiar el turno temporalmente para analizar al oponente
        self.move(movimiento.from_square, movimiento.to_square)
        retult = self.tablero1.is_check() or self.tablero2.is_check()
        self.pop()
        return retult

    def es_jaque_mate(self):
        """
        Determina si el jugador contrario está en jaque mate.
        Retorna True si hay jaque mate, False en caso contrario.
        """
        # Cambiar el turno temporalmente para analizar al oponente
        color_oponente = not self.color
        #self.tablero1.turn = color_oponente
        #self.tablero2.turn = color_oponente

        # Verificar si el rey del oponente está en jaque en cualquiera de los tableros
        rey_en_jaque = self.tablero1.is_check() or self.tablero2.is_check()
        movimientos_legales = []
        # Movimientos legales del tablero 1, verificando también jaque en tablero 2
        for move in self.tablero1.legal_moves:
            if not self.casilla_ocupada(self.tablero2, move.to_square):
                #self.tablero1.push(move)
                self.move(move.from_square, move.to_square)
                if not self.tablero1.is_check() or self.tablero2.is_check():  # No debe haber jaque al cambiar de tablero
                    movimientos_legales.append(move)
                #self.tablero1.pop()
                self.pop()

        # Movimientos legales del tablero 2, verificando también jaque en tablero 1
        for move in self.tablero2.legal_moves:
            if not self.casilla_ocupada(self.tablero1, move.to_square):
                #self.tablero2.push(move)
                self.move(move.from_square, move.to_square)
                if not self.tablero1.is_check() or self.tablero2.is_check():  # No debe haber jaque al cambiar de tablero
                    movimientos_legales.append(move)
                #self.tablero2.pop()
                self.pop()
        # Restaurar el turno original
        # self.tablero1.turn = self.color
        # self.tablero2.turn = self.color

        # Si el rey está en jaque y no hay movimientos legales, es jaque mate
        return rey_en_jaque and len(movimientos_legales) == 0

    
    def calcular_puntaje(self, color):
        def color_opuesto(color):
            return chess.BLACK if color == chess.WHITE else chess.WHITE

        def evaluar_tablero(tablero):
            score = 0
            for i in range(1, 7):
                piezas_color = tablero.pieces(i, color)
                # piezas_oponente = tablero.pieces(i, color_opuesto(color))

                # Sumar valores de piezas propias
                score += (len(piezas_color) * self.piece_values[i]) / 2
                for square in piezas_color:
                    score += (self.square_table[i][square]) / 10

                # Restar valores de piezas enemigas
                # score -= len(piezas_oponente) * self.piece_values[i]
                # for square in piezas_oponente:
                #     score -= self.square_table[i][square]

            return score

        score_tablero1 = evaluar_tablero(self.tablero1.copy())
        score_tablero2 = evaluar_tablero(self.tablero2.copy())

        return (score_tablero1 + score_tablero2) 

