from flask import Flask, render_template, jsonify, request
#from Proyecto.reglas_tablero import *
#from Proyecto.Minimax import *
from Proyecto.tablero_magico import tablero_magico
from Proyecto.IA_ajedrex import IA_Ajedrez
from Proyecto.Minimax import Minimax
import chess
import os
import time

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/move', methods=['POST'])
def get_move():
    try:
        data = request.get_json()
        fen = data['fen']
        fen2 = data['fen2']
        
        tablero1 = chess.Board(fen)
        tablero2 = chess.Board(fen2)
        # print("calculado")

        #movimiento = find_best_move(tablero_magico(tablero1.copy(),tablero2.copy(), chess.BLACK), 3)
        ia = Minimax(tablero_magico(tablero1.copy(),tablero2.copy(), chess.BLACK))
        inicio = time.time()
        movimiento = ia.iterative_deepening(4)
        fin = time.time()
        print(f"Tiempo transcurrido: {fin - inicio} segundos")
        tableroMagico = tablero_magico(tablero1.copy(), tablero2.copy(), chess.BLACK)
        print(movimiento)
        if tableroMagico.move(movimiento.from_square, movimiento.to_square):
            tablero1_nuevo, tablero2_nuevo = tableroMagico.get_tableros()
            print(tablero1_nuevo)
            print(tablero2_nuevo)
            print("fin")
            return jsonify({'tablero1': tablero1_nuevo.fen(), 'tablero2': tablero2_nuevo.fen()})
        return jsonify({'error': "xd"})
    # except ValueError as e:
    #     print(e)
    #     return jsonify({'error': str(e)}), 400
        
    except KeyError as e:
        print(e)
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400



@app.route('/validate_move', methods=['POST'])
def validate_move():
    try:
        # Obtener los datos del cuerpo de la solicitud
        data = request.get_json()
        fen = data['fen']
        fen2 = data['fen2']
        from_square = data['from_square']
        to_square = data['to_square']
        if not chess.Board(fen=fen) or not chess.Board(fen=fen2) or from_square == to_square:
            raise ValueError(f"Invalid FEN: {fen}")

        tablero1 = chess.Board(fen)
        tablero2 = chess.Board(fen2)
        tableroMagico = tablero_magico(tablero1.copy(),tablero2.copy(), chess.WHITE)
        origen = chess.parse_square(from_square)
        destino = chess.parse_square(to_square)
        seMovio = tableroMagico.move(origen,destino)
        tablero1_nuevo, tablero2_nuevo = tableroMagico.get_tableros()
        if seMovio:
            return jsonify({'tablero1': tablero1_nuevo.fen(), 'tablero2': tablero2_nuevo.fen()})
        return jsonify({'mobimiento invalido': "xd"}), 400

    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400
        
    except KeyError as e:
        print(e)
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400

@app.route('/puntaje/', methods=['POST'])
def puntaje(fen):
    fen = data['fen']
    fen2 = data['fen2']
    tableroMagico = tablero_magico(tablero1.copy(),tablero2.copy(), chess.WHITE)

    blancas = calcular_puntaje(tableroMagico, chess.WHITE)
    negras = calcular_puntaje(tableroMagico, chess.BLACK)
    #puntaje_blancas, puntaje_negras = contar_fichas(fen)
    return jsonify({
        'puntaje_blancas': blancas,
        'puntaje_negras': negras
    })


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester


def server():
    app.run(debug=True)