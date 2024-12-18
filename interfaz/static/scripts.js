var board, game = new Chess();
  // statusEl = $('#status'),

var board2, game2 = new Chess();

game2.clear();

var corriendo = false;


var onDrop = function(source, target) {
  if (corriendo) {
    console.warn("La función ya está en ejecución.");
    alert("esperando ia")
    return 'snapback';
  }
  console.log(corriendo);
  // board = Chessboard('board', {
  //   draggable: true,
  //   position: game.fen()
  // });
  // board2 = Chessboard('board', {
  //   draggable: true,
  //   position: game2.fen()
  // });

  corriendo = true; 

  $.ajax({
    url: $SCRIPT_ROOT + "/validate_move",
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        fen: game.fen(),
        fen2: game2.fen(),
        from_square: source,
        to_square: target
    }),
    success: function(response) {
        console.log(response);
        if (game.fen() !== response.tablero1 && game2.fen() !== response.tablero2){
            console.log(response.tablero1);
            console.log(response.tablero2);
            game.load(response.tablero1);
            game2.load(response.tablero2);
            board.position(game.fen());
            board2.position(game2.fen());
            updateStatus();
            getResponseMove();
            
        } else {
            corriendo = false; 
            return 'snapback';
        }
    },
    error: function(xhr, status, error) {
        corriendo = false;
        console.error("Error: " + error);
        console.error("Response: " + xhr.responseText);
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

  // Llamada AJAX para obtener el puntaje
  $.ajax({
    url: $SCRIPT_ROOT + "/puntaje",
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
        fen: game.fen(),
        fen2: game2.fen(),
    }),
    success: function(response){
      // Mostrar los puntajes obtenidos en la respuesta
      var puntajeBlancas = response.puntaje_blancas;
      var puntajeNegras = response.puntaje_negras;
      // checkmate?
      // if (game.in_checkmate() === true || game2.in_checkmate() === true) {
      //   $('#puntaje_blancas').text('Game over, is in checkmate.');
      // } else{
      $('#puntaje_blancas').text('Puntaje Blancas: ' + puntajeBlancas);
      $('#puntaje_negras').text('Puntaje Negras: ' + puntajeNegras);

    },
    
    error: function(xhr, status, error) {
        console.error("Error: " + error);
        console.error("Response: " + xhr.responseText);
    },
    
    // Aquí puedes actualizar el HTML con los puntajes
    
  });

};


var getResponseMove = function() {
    $.ajax({
      url: $SCRIPT_ROOT + "/move",
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
          fen: game.fen(),
          fen2: game2.fen(),
      }),
      success: function(response) {
          console.log(response);
          game.load(response.tablero1);
          game2.load(response.tablero2);
          setTimeout(function(){ 
            board.position(game.fen()); 
            board2.position(game2.fen());
          }, 100);
          corriendo = false;
          // board.position(game.fen());
          // board2.position(game2.fen());
      },
      error: function(xhr, status, error) {
          console.error("Error: " + error);
          console.error("Response: " + xhr.responseText);
          corriendo = false;
      },
      complete: function() {
        // Asegurarse de que el estado `corriendo` se desbloquee en caso de error también.
        
        // board = ChessBoard('board', cfg);
        // board2 = ChessBoard('board2', cfg2);
      } 
    })
    
}


// did this based on a stackoverflow answer
// http://stackoverflow.com/questions/29493624/cant-display-board-whereas-the-id-is-same-when-i-use-chessboard-js
setTimeout(function() {
    board = ChessBoard('board', cfg);
    board2 = ChessBoard('board2', cfg2);
    updateStatus();
}, 0);


var cfg = {
  draggable: true,
  position: 'start',
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
};

// ============================================== tablero 2

var cfg2 = {
  draggable: true,
  position: 'empty', // Configura el tablero para que inicie vacío1
  onDrop: onDrop,
  onSnapEnd: function() {
      board2.position(game2.fen());
  }
};

var takeBack = function() {
  game.undo();
  game2.undo();
  board.position(game.fen());
  board2.position(game2.fen());
  updateStatus();
}


// var cfg = {
//   draggable: true,
//   position: 'start',
//   onDragStart: onDragStart,
//   onDrop: onDrop,
//   onSnapEnd: onSnapEnd
// };


// var randomResponse = function() {
//     fen = game.fen()
//     $.get($SCRIPT_ROOT + "/move/" + fen, function(data) {
//         game.move(data, {sloppy: true});
//         // board.position(game.fen());
//         updateStatus();
//     })
// }



// var getCapturedPieces = function() {
//     var history = game.history({ verbose: true });
//     for (var i = 0; i < history.length; i++) {
//         if ("captured" in history[i]) {
//             console.log(history[i]["captured"]);
//         }
//     }
// }

// var getLastCapture = function() {
//     var history = game.history({ verbose: true });
//     var index = history.length - 1;

//     if (history[index] != undefined && "captured" in history[index]) {
//         console.log(history[index]["captured"]);
//     }
// }

// var takeBack = function() {
//     game.undo();
//     if (game.turn() != "w") {
//         game.undo();
//     }
//     board.position(game.fen());
//     updateStatus();
// }

// var newGame = function() {
//     game.reset();
//     board.start();
//     updateStatus();
// }
