import chess
import random
import signal
import time
import cProfile

class Minimax:

    def __init__(self, magicBOard):
        self.board = magicBOard
        self.MAX_DEPTH = 60
        self.transposition_table = {}
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
        self.square_table = square_table = {
            1: [
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
        # self.board.set_fen(fen)
        self.leaves_reached = 0

    def generar_clave_tablero(self, tableroMagico):
        """
        Genera una clave única para el tablero actual.
        """
        return hash(tableroMagico.fen())


    def position_eval(self, tableroMagico):
        def evaluar_tablero(tablero):
            score = 0
            # iterate through the pieces
            for i in range(1, 7):
                # eval white pieces
                w_squares = tablero.pieces(i, chess.WHITE)
                score += len(w_squares) * self.piece_values[i]
                for square in w_squares:
                    score += self.square_table[i][-square]

                b_squares = tablero.pieces(i, chess.BLACK)
                score -= len(b_squares) * self.piece_values[i]
                for square in b_squares:
                    score -= self.square_table[i][square]

            return score

        valor_negras = evaluar_tablero(tableroMagico.tablero1) + evaluar_tablero(tableroMagico.tablero2)
        #sincronizacion = len(tableroMagico.generar_movimientos())
        #jaques = 2 if tableroMagico.es_jaque() else 0

        return valor_negras



    def minimax(self, depth_neg, depth_pos, move, alpha, beta, prev_moves, maximiser, tablero):
        clave = (self.generar_clave_tablero(tablero), maximiser)
        
        move_sequence = []

        # check if we're at the final search depth
        if depth_neg == 0:
            # return move, self.material_eval()
            move_sequence.append(move)
            return move_sequence, self.position_eval(tablero)


        moves = list(tablero.generar_movimientos())
    

        # if there are no legal moves, check for checkmate / stalemate
        if not moves:
            if tablero.is_checkmate():
                if tablero.result() == "1-0":
                    move_sequence.append(move)
                    return move_sequence, 1000000
                elif tablero.result() == "0-1":
                    move_sequence.append(move)
                    return move_sequence, -1000000
            else:
                move_sequence.append(move)
                return move_sequence, 0
        
        # initialise best move variables. What are these used for again? I need to simplify the logic here.
        best_move = None
        best_score = -10000001 if maximiser else 10000001

        # put the last calculated best move in first place of the list. Hopefully this improves pruning.
        if prev_moves and len(prev_moves) >= depth_neg:
            if depth_neg == 4 and not tablero.color:
                print(prev_moves[depth_neg - 1])
            if prev_moves[depth_neg - 1] in moves:
            # if prev_moves[depth_neg - 1] in self.board.legal_moves:
                # if not self.board.turn:
                #     print(prev_moves[depth_neg - 1])
                moves.insert(0, prev_moves[depth_neg - 1])

        if clave in self.transposition_table:
            score, move = self.transposition_table[clave]
            return move, score

        if maximiser:
            for move in moves:
                self.leaves_reached += 1

                # get score of the new move, record what it is
                if tablero.move(move.from_square, move.to_square):
                    new_sequence, new_score = self.minimax(depth_neg - 1, depth_pos + 1, move, alpha, beta, prev_moves, False, tablero.copy())
                    tablero.pop()

                    # Check whether the new score is better than the best score. If so, replace the best score.
                    if new_score > best_score:
                        move_sequence = new_sequence
                        best_score, best_move = new_score, move

                    # Check whether the new score is better than the beta. If it is, return and break the loop.
                    # Need to rethink the check against best here.
                    if new_score >= beta:
                        # self.check_against_best(best_move, best_score, depth_pos, True)
                        move_sequence.append(best_move)
                        return move_sequence, best_score
                    # Update alpha - upper bound
                    if new_score > alpha:
                        alpha = new_score
            # return the best of the results
            # self.check_against_best(best_move, best_score, depth_pos, True)
            move_sequence.append(best_score)
            # print(best_move, best_score)
            # exit()
            self.transposition_table[clave] = (best_score, move_sequence)

            return move_sequence, best_score

        if not maximiser:
            for move in moves:
                self.leaves_reached += 1

                # get score of the new move, record what it is
                if tablero.move(move.from_square, move.to_square):
                    new_sequence, new_score = self.minimax(depth_neg - 1, depth_pos + 1, move, alpha, beta, prev_moves, True, tablero.copy())
                    tablero.pop()

                    # Check whether the new score is better than the best score. If so, replace the best score.
                    if new_score < best_score:
                        move_sequence = new_sequence
                        best_score, best_move = new_score, move

                    # Check whether the new score is better than the alpha. If it is, return and break the loop
                    if new_score <= alpha:
                        # self.check_against_best(best_move, best_score, depth_pos, False)
                        move_sequence.append(best_move)
                        return move_sequence, best_score

                    # update beta - lower bound
                    if new_score < beta:
                        beta = new_score

            # return the best of the results
            # self.check_against_best(best_move, best_score, depth_pos, False)
            move_sequence.append(best_move)
            self.transposition_table[clave] = (best_score, move_sequence)
            return move_sequence, best_score

    
    def iterative_deepening(self, depth):
        # depth_neg, depth_pos, move, alpha, beta, prev_moves, maximiser)
        move_list, score  = self.minimax(1, 0, None, -10000001, 10000001, None, self.board.color, self.board)
        print(self.board.fen())
        print("boards")
        print(self.board.color)
        for i in range(2, depth + 1):
            print("Iteration", i)
            print(self.board.color)
            move_list, score = self.minimax(i, 0, None, -10000001, 10000001, move_list, self.board.color, self.board)
        print("boards")
        print("Depth calculated:", move_list)
        print(self.board.fen())
        return move_list[-1]


