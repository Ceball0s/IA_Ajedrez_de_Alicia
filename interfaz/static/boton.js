document.getElementById("turnoButton").addEventListener("click", () => {
    if (corriendo) {
        corriendo = false;
        // document.getElementById("status").innerText = "Estado: Corriendo";
        // console.log("Turno solicitado. Ahora está corriendo.");
    } else {
        // console.log("Ya está corriendo. No se puede pedir otro turno.");
    }
  });