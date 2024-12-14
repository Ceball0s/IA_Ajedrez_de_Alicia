from flask import Flask, render_template, jsonify, request
#from Proyecto.reglas_tablero import *
from Proyecto.Minimax import *
from Proyecto.tablero_magico import tablero_magico
import os

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
        print("calculado")
        movimiento = find_best_move(tablero_magico(tablero1.copy(),tablero2.copy(), chess.BLACK), 3)
        tableroMagico = tablero_magico(tablero1,tablero2, chess.BLACK)
        print(movimiento)
        tableroMagico.move(movimiento.from_square, movimiento.to_square)
        return jsonify({'tablero1': tablero1.fen(), 'tablero2': tablero2.fen()})

    # except ValueError as e:
    #     print(e)
    #     return jsonify({'error': str(e)}), 400
        
    except KeyError as e:
        print(e)
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester

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
        tableroMagico = tablero_magico(tablero1,tablero2, chess.WHITE)
        origen = chess.parse_square(from_square)
        destino = chess.parse_square(to_square)
        tableroMagico.move(origen,destino)
        tablero1, tablero2 = tableroMagico.get_tableros()
        return jsonify({'tablero1': tablero1.fen(), 'tablero2': tablero2.fen()})

    except ValueError as e:
        print(e)
        return jsonify({'error': str(e)}), 400
        
    except KeyError as e:
        print(e)
        return jsonify({'error': f'Missing parameter: {str(e)}'}), 400

@app.route('/puntaje/<path:fen>')
def puntaje(fen):
    #puntaje_blancas, puntaje_negras = contar_fichas(fen)
    return jsonify({
        'puntaje_blancas': 0,
        'puntaje_negras': 0
    })


def server():
    app.run(debug=True)