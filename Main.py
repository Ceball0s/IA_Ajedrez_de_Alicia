import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interfaz.flask_app import server  # Importar servidor
# from test.test_punto1 import medir_tiempos_terminal
# from test.test_punto2 import medir_tiempos_subasta
# from test.test_punto2 import generar_datos_subasta

# def ejecutar_tests():
#     print("== test terminal")
#     for longitud in [5, 10, 15, 20]:  
#         medir_tiempos_terminal(longitud)

#     for longitud in [2, 6, 12, 16]:
#         A, B, ofertas = generar_datos_subasta(num_ofertas=longitud, max_precio=150*longitud)
#         medir_tiempos_subasta(A, B, ofertas)

if __name__ == "__main__":
    if "--performance-test" in sys.argv:
        # ejecutar_tests()
        pass
    else:
        print("Iniciando el servidor...")
        server()
