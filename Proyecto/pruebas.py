from Proyecto.tablero_magico import tablero_magico

def probar_pop(tablero_magico_obj):
    """
    Prueba si la función `pop` en `tablero_magico` restaura correctamente los tableros.
    """
    # Copiar los estados iniciales
    tablero1_inicial = tablero_magico_obj.tablero1.copy()
    tablero2_inicial = tablero_magico_obj.tablero2.copy()
    print(tablero1_inicial)

    # Generar un movimiento válido
    movimientos = tablero_magico_obj.generar_movimientos()
    if not movimientos:
        print("No hay movimientos legales para probar.")
        return False

    #movimiento = movimientos[0]  # Elegir un movimiento cualquiera
    for movimiento in movimientos:
        # Realizar el movimiento
        if not tablero_magico_obj.move(movimiento.from_square, movimiento.to_square):
            print("no")

        # Verificar que los tableros hayan cambiado
        if tablero_magico_obj.tablero1 == tablero1_inicial and tablero_magico_obj.tablero2 == tablero2_inicial:
            print("Error: Los tableros no cambiaron después del movimiento.")
            return False

        # Aplicar `pop` para deshacer el movimiento
        tablero_magico_obj.pop()

        # Verificar si los tableros volvieron al estado original
        if tablero_magico_obj.tablero1 == tablero1_inicial and tablero_magico_obj.tablero2 == tablero2_inicial:
            print("`pop` funciona correctamente: los tableros fueron restaurados.")
            return True
        else:
            print("Error: `pop` no restauró correctamente los tableros.")
            return False


import chess

# Crear dos tableros y configurarlos
tablero1 = chess.Board()
tablero2 = chess.Board()

# Crear el objeto `tablero_magico`
tablero_magico_obj = tablero_magico(tablero1, tablero2, chess.BLACK)

# Probar `pop`
resultado = probar_pop(tablero_magico_obj)
print("Resultado de la prueba:", "Correcto" if resultado else "Incorrecto")
