from flask import Flask, render_template, jsonify
from Proyecto.reglas_tablero import *
from Proyecto.Minimax import *
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/move/<int:depth>/<path:fen>/')
def get_move(depth, fen):
    print(depth)
    print(fen)
    print("Calculating...")
    board = chess.Board(fen)
    move = find_best_move(board, 4)
    move = move.uci() 
    print("Move found!", move)
    print()
    return move


@app.route('/test/<string:tester>')
def test_get(tester):
    return tester

@app.route('/validate_move/<path:fen>/<from_square>/<to_square>/')
def validate_move(fen, from_square, to_square):
    nuevo_fen, score_blancas, score_negras = verificar_movimiento_pierde_gana(fen,from_square+to_square)
    return nuevo_fen

@app.route('/puntaje/<path:fen>')
def puntaje(fen):
    puntaje_blancas, puntaje_negras = contar_fichas(fen)
    return jsonify({
        'puntaje_blancas': puntaje_blancas,
        'puntaje_negras': puntaje_negras
    })


def server():
    app.run(debug=True)