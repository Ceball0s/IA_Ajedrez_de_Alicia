var board, game = new Chess(),fenEl = $('#fen'),pgnEl = $('#pgn');
  // statusEl = $('#status'),

var board2, game2 = new Chess();

// do not pick up pieces if the game is over
// only pick up pieces for the side to move
var onDragStart = function(source, piece, position, orientation) {
  if (game.game_over() === true ||
      (game.turn() === 'w' && piece.search(/^b/) !== -1) ||
      (game.turn() === 'b' && piece.search(/^w/) !== -1)) {
    return false;
  }
};

var onDrop = function(source, target) {
  // var move = game.push({
  //   from: source,
  //   to: target,
  //   promotion: 'q' // NOTE: always promote to a queen for example simplicity
  // });

  // Enviar el movimiento al servidor para verificar si es válido
  $.ajax({
    url: $SCRIPT_ROOT + "/validate_move/" + game.fen() + "/" + source + "/" + target,
    method: 'GET',
    success: function(fen) {
      console.log(fen);
      status = 'hola';
      
      if (game.fen() !== fen){
        game.load(fen);
        updateStatus();
        getResponseMove();
      } else{
        return 'snapback';
      }
    },
    error: function() {
      console.log('Error al verificar el movimiento');
    }
  });
};


// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
    board.position(game.fen());
};

// Función para actualizar el puntaje
var updateStatus = function() {
  var status = '';
  var moveColor = 'White';

  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // Llamada AJAX para obtener el puntaje
  $.get($SCRIPT_ROOT + "/puntaje/" + game.fen(), function(data) {
    // Mostrar los puntajes obtenidos en la respuesta
    var puntajeBlancas = data.puntaje_blancas;
    var puntajeNegras = data.puntaje_negras;

    // Aquí puedes actualizar el HTML con los puntajes
    $('#puntaje_blancas').text('Puntaje Blancas: ' + puntajeBlancas);
    $('#puntaje_negras').text('Puntaje Negras: ' + puntajeNegras);
  });

  // Lógica de juego como estaba
  if (game.turn() === 'b') {
    moveColor = 'Black';
  }

  // Comprobar estado del juego
  if (game.in_checkmate() === true) {
    status = 'Game over, ' + moveColor + ' is in checkmate.';
  } else if (game.in_draw() === true) {
    status = 'Game over, drawn position';
  } else {
    status = moveColor + ' to move';
    if (game.in_check() === true) {
      status += ', ' + moveColor + ' is in check';
    }
  }

  // setStatus(status);
  getLastCapture();
  createTable();
  // updateScroll();

  // statusEl.html(status);
  fenEl.html(game.fen());
  pgnEl.html(game.pgn());
};


// var cfg = {
//   draggable: true,
//   position: 'start',
//   onDragStart: onDragStart,
//   onDrop: onDrop,
//   onSnapEnd: onSnapEnd
// };
var cfg = {
  draggable: true,
  position: 'start',
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};

var randomResponse = function() {
    fen = game.fen()
    $.get($SCRIPT_ROOT + "/move/" + fen, function(data) {
        game.move(data, {sloppy: true});
        // board.position(game.fen());
        updateStatus();
    })
}

var getResponseMove = function() {
    var e = document.getElementById("sel1");
    var depth = 0; // implementado en el back
    fen = game.fen()
    $.get($SCRIPT_ROOT + "/move/" + depth + "/" + fen, function(data) {
        game.move(data, {sloppy: true});
        updateStatus();
        // This is terrible and I should feel bad. Find some way to fix this properly.
        // The animations would stutter when moves were returned too quick, so I added a 100ms delay before the animation
        setTimeout(function(){ board.position(game.fen()); }, 100);
    })
}


// did this based on a stackoverflow answer
// http://stackoverflow.com/questions/29493624/cant-display-board-whereas-the-id-is-same-when-i-use-chessboard-js
setTimeout(function() {
    board = ChessBoard('board', cfg);
    // updateStatus();
}, 0);


var setPGN = function() {
  var table = document.getElementById("pgn");
  var pgn = game.pgn().split(" ");
  var move = pgn[pgn.length - 1];
}

var createTable = function() {

    var pgn = game.pgn().split(" ");
    var data = [];

    for (i = 0; i < pgn.length; i += 3) {
        var index = i / 3;
        data[index] = {};
        for (j = 0; j < 3; j++) {
            var label = "";
            if (j === 0) {
                label = "moveNumber";
            } else if (j === 1) {
                label = "whiteMove";
            } else if (j === 2) {
                label = "blackMove";
            }
            if (pgn.length > i + j) {
                data[index][label] = pgn[i + j];
            } else {
                data[index][label] = "";
            }
        }
    }

    $('#pgn tr').not(':first').remove();
    var html = '';
    for (var i = 0; i < data.length; i++) {
        html += '<tr><td>' + data[i].moveNumber + '</td><td>'
        + data[i].whiteMove + '</td><td>'
        + data[i].blackMove + '</td></tr>';
    }

    $('#pgn tr').first().after(html);
}

// var updateScroll = function() {
//     $('#moveTable').scrollTop($('#moveTable')[0].scrollHeight);
// }

// var setStatus = function(status) {
//   document.getElementById("status").innerHTML = status;
// }

var takeBack = function() {
    game.undo();
    if (game.turn() != "w") {
        game.undo();
    }
    board.position(game.fen());
    updateStatus();
}

var newGame = function() {
    game.reset();
    board.start();
    updateStatus();
}

var getCapturedPieces = function() {
    var history = game.history({ verbose: true });
    for (var i = 0; i < history.length; i++) {
        if ("captured" in history[i]) {
            console.log(history[i]["captured"]);
        }
    }
}

var getLastCapture = function() {
    var history = game.history({ verbose: true });
    var index = history.length - 1;

    if (history[index] != undefined && "captured" in history[index]) {
        console.log(history[index]["captured"]);
    }
}


// ============================================== tablero 2

var cfg2 = {
  draggable: true,
  onDrop: function(source, target) {
      // Similar lógica al onDrop original
      var move = game2.move({
          from: source,
          to: target,
          promotion: 'q' // Promoción por simplicidad
      });

      if (move === null) return 'snapback'; // Movimiento inválido
      updateStatus2();
  },
  onSnapEnd: function() {
      board2.position(game2.fen());
  }
};

setTimeout(function() {
  board2 = ChessBoard('board2', cfg2);
}, 0);